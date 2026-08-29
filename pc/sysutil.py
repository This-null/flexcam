import json
import os
import shutil
import subprocess
import sys
import tempfile
import webbrowser
import zipfile
from urllib.request import Request, urlopen

import config


def _base_dir():
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def virtualcam_installer():
    p = os.path.join(_base_dir(), "virtualcam", "Install.bat")
    return p if os.path.exists(p) else None


def install_virtualcam():
    p = virtualcam_installer()
    if not p:
        return False
    try:
        os.startfile(p)
        return True
    except Exception:
        return False


def open_url(url):
    try:
        webbrowser.open(url)
    except Exception:
        pass


def obs_installed():
    candidates = [
        os.path.expandvars(r"%ProgramFiles%\obs-studio\bin"),
        os.path.expandvars(r"%ProgramFiles(x86)%\obs-studio\bin"),
    ]
    return any(os.path.isdir(p) for p in candidates)


def _ver_tuple(v):
    parts = []
    for p in str(v).split("."):
        try:
            parts.append(int(p))
        except ValueError:
            parts.append(0)
    return tuple(parts)


def check_update():
    try:
        with urlopen(config.UPDATE_URL, timeout=4) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return False, None, None
    latest = data.get("version")
    url = data.get("url", config.GITHUB_URL)
    if latest and _ver_tuple(latest) > _ver_tuple(config.APP_VERSION):
        return True, latest, url
    return False, latest, url


def can_self_update():
    if not getattr(sys, "frozen", False):
        return False
    target = install_dir()
    probe = os.path.join(target, ".flexcam_write_test")
    try:
        with open(probe, "w") as f:
            f.write("1")
        os.remove(probe)
        return True
    except Exception:
        return False


def install_dir():
    return os.path.dirname(os.path.abspath(sys.executable))


def latest_zip_url():
    try:
        req = Request(config.RELEASES_API, headers={"User-Agent": "FlexCam"})
        with urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None
    for asset in data.get("assets", []):
        name = str(asset.get("name", "")).lower()
        if name.endswith(".zip"):
            return asset.get("browser_download_url")
    return None


def download_update(url, on_progress=None):
    tmp_root = tempfile.mkdtemp(prefix="flexcam_update_")
    zip_path = os.path.join(tmp_root, "update.zip")
    try:
        req = Request(url, headers={"User-Agent": "FlexCam"})
        with urlopen(req, timeout=30) as resp:
            total = int(resp.headers.get("Content-Length") or 0)
            done = 0
            with open(zip_path, "wb") as f:
                while True:
                    chunk = resp.read(262144)
                    if not chunk:
                        break
                    f.write(chunk)
                    done += len(chunk)
                    if on_progress and total:
                        on_progress(int(done * 100 / total))
        if total and os.path.getsize(zip_path) < total:
            raise IOError("incomplete download")
        return tmp_root, zip_path
    except Exception:
        shutil.rmtree(tmp_root, ignore_errors=True)
        return None, None


def extract_update(tmp_root, zip_path):
    out = os.path.join(tmp_root, "new")
    try:
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(out)
    except Exception:
        return None
    exe = os.path.basename(sys.executable)
    for root, _dirs, files in os.walk(out):
        if exe in files:
            return root
    return None


def apply_update(new_dir, tmp_root, restart=True):
    target = install_dir()
    exe = os.path.join(target, os.path.basename(sys.executable))
    bat = os.path.join(tmp_root, "apply.bat")
    launch = f'start "" "{exe}"' if restart else "rem no restart"
    name = os.path.basename(sys.executable)
    script = (
        "@echo off\r\n"
        "setlocal\r\n"
        "set SYS=%SystemRoot%\\System32\r\n"
        "set /a N=0\r\n"
        ":wait\r\n"
        "set /a N+=1\r\n"
        "if %N% GTR 600 goto copy\r\n"
        f'"%SYS%\\tasklist.exe" /fi "IMAGENAME eq {name}" /nh 2>nul | '
        f'"%SYS%\\find.exe" /i "{name}" >nul\r\n'
        "if not errorlevel 1 (\r\n"
        '  "%SYS%\\ping.exe" -n 2 127.0.0.1 >nul\r\n'
        "  goto wait\r\n"
        ")\r\n"
        ":copy\r\n"
        f'"%SYS%\\robocopy.exe" "{new_dir}" "{target}" /E /IS /R:2 /W:1 >nul\r\n'
        f"{launch}\r\n"
        '"%SYS%\\ping.exe" -n 3 127.0.0.1 >nul\r\n'
        f'rmdir /s /q "{tmp_root}"\r\n'
    )
    try:
        with open(bat, "w", encoding="ascii", newline="") as f:
            f.write(script)
        subprocess.Popen(
            [os.path.join(os.environ.get("SystemRoot", r"C:\Windows"),
                          "System32", "cmd.exe"), "/c", bat],
            creationflags=0x08000000,
            close_fds=True,
        )
        return True
    except Exception:
        return False


def settings_path():
    base = os.path.join(os.path.expanduser("~"), ".flexcam")
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, "settings.json")


def load_settings():
    try:
        with open(settings_path(), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_settings(data):
    try:
        with open(settings_path(), "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception:
        pass
