import threading
import time
from http.client import HTTPConnection

from mjpeg_client import MjpegParser
from virtual_cam import VirtualCamera, jpeg_to_rgb
import adb_tools

PORT = 8474


def _stream(host, timeout=2):
    conn = HTTPConnection(host, PORT, timeout=timeout)
    conn.request("GET", "/")
    resp = conn.getresponse()
    if resp.status != 200:
        raise RuntimeError(f"HTTP {resp.status}")
    parser = MjpegParser()
    while True:
        chunk = resp.read(4096)
        if not chunk:
            return
        parser.feed(chunk)
        for jpeg in parser.frames():
            yield jpeg


def _control(host, cmd):
    try:
        conn = HTTPConnection(host, PORT, timeout=1.5)
        conn.request("GET", "/" + cmd)
        conn.getresponse().read()
        conn.close()
    except Exception:
        pass


class FlexCamEngine:
    def __init__(self, wifi_ip=None, on_status=None):
        self._wifi_ip = wifi_ip
        self._on_status = on_status or (lambda *a: None)
        self._thread = None
        self._running = False
        self._active_host = None

    def is_running(self):
        return self._running

    def set_wifi_ip(self, ip):
        self._wifi_ip = ip

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

    def _sources(self):
        src = [{"name": "USB", "host": "127.0.0.1", "usb": True}]
        if self._wifi_ip:
            src.append({"name": "WiFi", "host": self._wifi_ip, "usb": False})
        return src

    def _loop(self):
        cam = None
        attempts = 0
        while self._running and cam is None:
            try:
                cam = VirtualCamera(fps=30)
            except Exception as e:
                attempts += 1
                if attempts >= 3:
                    self._on_status("error", None, self._camera_error(e))
                else:
                    self._on_status("starting", None, "")
                time.sleep(1.5)
        if not self._running or cam is None:
            self._running = False
            self._on_status("stopped", None, "")
            return

        self._on_status("searching", None, "")
        active = None
        idx = 0
        try:
            while self._running:
                sources = self._sources()
                src = sources[idx % len(sources)]
                idx += 1
                try:
                    if src["usb"]:
                        if not adb_tools.ensure_forward():
                            continue
                    _control(src["host"], "start")
                    for jpeg in _stream(src["host"]):
                        if not self._running:
                            break
                        if active != src["name"]:
                            active = src["name"]
                            self._active_host = src["host"]
                            self._on_status("connected", active, "")
                        cam.send(jpeg_to_rgb(jpeg))
                    active = None
                except Exception:
                    if active == src["name"]:
                        self._on_status("searching", None, "")
                    active = None
                if self._running:
                    time.sleep(1)
        finally:
            cam.close()
            if self._active_host:
                _control(self._active_host, "stop")
                self._active_host = None
            self._running = False
            self._on_status("stopped", None, "")

    @staticmethod
    def _camera_error(e):
        msg = str(e)
        if "could not be started" in msg or "No camera registered" in msg:
            return "no_camera"
        return "camera_generic"
