import os
import subprocess
import sys

PORT = 8474

NO_WINDOW = 0
if os.name == "nt":
    NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def _base_dir():
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def adb_path():
    bundled = os.path.join(_base_dir(), "adb", "adb.exe")
    if os.path.exists(bundled):
        return bundled
    sdk = os.path.expandvars(
        r"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe"
    )
    if os.path.exists(sdk):
        return sdk
    return "adb"


def apk_path():
    candidates = [
        os.path.join(_base_dir(), "FlexCam.apk"),
        os.path.join(_base_dir(), "..", "release", "FlexCam.apk"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return os.path.abspath(c)
    return None


def _run(args, timeout=15):
    return subprocess.run(
        [adb_path(), *args],
        capture_output=True, text=True, timeout=timeout,
        creationflags=NO_WINDOW,
    )


def detect_device():
    try:
        out = _run(["devices"], timeout=6).stdout
    except Exception:
        return None
    for line in out.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device" \
                and not parts[0].startswith("emulator-"):
            return parts[0]
    return None


def app_installed(serial=None):
    serial = serial or detect_device()
    if serial is None:
        return False
    try:
        out = _run(["-s", serial, "shell", "pm", "list", "packages",
                    "com.flexcam"], timeout=6).stdout
    except Exception:
        return False
    return "com.flexcam" in out


def ensure_forward():
    serial = detect_device()
    if serial is None:
        return False
    try:
        r = _run(["-s", serial, "forward", f"tcp:{PORT}", f"tcp:{PORT}"])
        return r.returncode == 0
    except Exception:
        return False


def install_apk():
    path = apk_path()
    if path is None:
        return False, "no_apk"
    serial = detect_device()
    if serial is None:
        return False, "no_device"
    try:
        r = _run(["-s", serial, "install", "-r", path], timeout=120)
    except Exception as e:
        return False, str(e)
    if "Success" in (r.stdout + r.stderr):
        return True, "install_ok"
    return False, (r.stderr or r.stdout).strip()
