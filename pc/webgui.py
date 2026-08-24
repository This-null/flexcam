import json
import os
import sys
import threading

import webview

from engine import FlexCamEngine
import adb_tools
import sysutil
import config
import i18n
import presence
import preview_server


def base_dir():
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def web_index():
    return os.path.join(base_dir(), "web", "index.html")


def logo_path():
    for p in (os.path.join(base_dir(), "web", "flexcam-logo.png"),
              os.path.join(base_dir(), "flexcam-logo.png")):
        if os.path.exists(p):
            return p
    return None


_WINDOW = None


class Api:
    def __init__(self):
        self.engine = FlexCamEngine(on_status=self._on_status)
        self.settings = sysutil.load_settings()
        self.t = i18n.T(self.settings.get("lang"))

    def _strings(self):
        strings = dict(i18n.STRINGS["en"])
        strings.update(i18n.STRINGS.get(self.t.lang, {}))
        return strings

    def get_bootstrap(self):
        return {
            "strings": self._strings(),
            "lang": self.t.lang,
            "langs": i18n.LANGS,
            "github": config.GITHUB_URL,
            "instagram": config.INSTAGRAM_URL,
            "discord": config.DISCORD_URL,
            "donate": config.DONATE_URL,
            "obs_url": config.OBS_DOWNLOAD_URL,
            "version": config.APP_VERSION,
            "obs_installed": sysutil.obs_installed(),
            "vcam_ready": sysutil.obs_installed() or self.settings.get("vcam_installed", False),
            "has_installer": sysutil.virtualcam_installer() is not None,
            "tray": self.settings.get("tray", True),
            "running": self.engine.is_running(),
            "wifi_ip": self.settings.get("wifi_ip", ""),
            "wifi_key": self.settings.get("wifi_key", ""),
        }

    def set_lang(self, lang):
        self.t = i18n.T(lang)
        self.settings["lang"] = self.t.lang
        sysutil.save_settings(self.settings)
        return {"strings": self._strings(), "lang": self.t.lang}

    def start(self, ip, key=""):
        ip = (ip or "").strip()
        key = (key or "").strip()
        self.settings["wifi_ip"] = ip
        self.settings["wifi_key"] = key
        sysutil.save_settings(self.settings)
        self.engine.set_wifi_ip(ip or None)
        self.engine.set_key(key)
        self.engine.start()

    def stop(self):
        self.engine.stop()

    def install_apk(self):
        ok, key = adb_tools.install_apk()
        return {"ok": ok, "key": key}

    def open_url(self, url):
        sysutil.open_url(url)

    def install_virtualcam(self):
        ok = sysutil.install_virtualcam()
        if ok:
            self.settings["vcam_installed"] = True
            sysutil.save_settings(self.settings)
        return ok

    def usb_connected(self):
        return adb_tools.detect_device() is not None

    def phone_status(self):
        serial = adb_tools.detect_device()
        return {
            "usb": serial is not None,
            "app": adb_tools.app_installed(serial) if serial else False,
        }

    def check_update(self):
        has, latest, url = sysutil.check_update()
        return {"has": has, "latest": latest, "url": url}

    def save_setting(self, key, val):
        self.settings[key] = val
        sysutil.save_settings(self.settings)

    def _on_status(self, state, info, _detail):
        w = _WINDOW
        if w is not None:
            try:
                w.evaluate_js(
                    f"window.flexStatus({json.dumps(state)}, {json.dumps(info)})"
                )
            except Exception:
                pass


class TrayHolder:
    def __init__(self, api, window):
        self.api = api
        self.window = window
        self.icon = None
        self.quitting = False

    def on_closing(self):
        if self.quitting:
            return True
        if self.api.settings.get("tray", True):
            self.window.hide()
            self._ensure_icon()
            return False
        self.api.engine.stop()
        return True

    def _ensure_icon(self):
        if self.icon is not None:
            return
        try:
            import pystray
            from PIL import Image
            path = logo_path()
            image = Image.open(path) if path else Image.new("RGB", (64, 64),
                                                            (91, 108, 255))
            menu = pystray.Menu(
                pystray.MenuItem(self.api.t("tray_show"), self._show,
                                 default=True),
                pystray.MenuItem(self.api.t("tray_quit"), self._quit),
            )
            self.icon = pystray.Icon("flexcam", image, "FlexCam", menu)
            threading.Thread(target=self.icon.run, daemon=True).start()
        except Exception:
            self.window.show()

    def _show(self, *a):
        self.window.show()

    def _quit(self, *a):
        self.quitting = True
        self.api.engine.stop()
        if self.icon is not None:
            try:
                self.icon.stop()
            except Exception:
                pass
        self.window.destroy()


def main():
    global _WINDOW
    api = Api()
    window = webview.create_window(
        "FlexCam", url=web_index(), js_api=api,
        width=1120, height=760, min_size=(900, 640),
        background_color="#14161f",
    )
    _WINDOW = window
    tray = TrayHolder(api, window)
    window.events.closing += tray.on_closing
    preview_server.PreviewServer(lambda: api.engine.preview_jpeg()).start()
    presence.start()
    webview.start()


if __name__ == "__main__":
    main()
