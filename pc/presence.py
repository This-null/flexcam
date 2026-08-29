import threading
import time

import config


def _payload(start):
    return dict(
        details="Phone as a webcam",
        state="USB / WiFi",
        start=start,
        large_image="flexcam",
        large_text="FlexCam",
        large_url=config.GITHUB_URL,
        buttons=[
            {"label": "GitHub", "url": config.GITHUB_URL},
            {"label": "Download", "url": config.DOWNLOAD_URL},
        ],
    )


def _run():
    try:
        from pypresence import Presence
    except Exception:
        return
    if not config.DISCORD_CLIENT_ID:
        return
    while True:
        try:
            rpc = Presence(config.DISCORD_CLIENT_ID)
            rpc.connect()
            start = int(time.time())
            data = _payload(start)
            try:
                rpc.update(**data)
            except TypeError:
                data.pop("large_url", None)
                try:
                    rpc.update(**data)
                except TypeError:
                    data.pop("buttons", None)
                    rpc.update(**data)
            while True:
                time.sleep(15)
        except Exception:
            time.sleep(30)


def start():
    threading.Thread(target=_run, daemon=True).start()
