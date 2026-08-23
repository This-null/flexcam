import json
import os
import webbrowser
from urllib.request import urlopen

import config


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
