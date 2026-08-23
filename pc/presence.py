import threading
import time

import config


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
            rpc.update(
                details="Phone as a webcam",
                state="USB / WiFi",
                start=start,
                large_image="flexcam",
                large_text="FlexCam",
            )
            while True:
                time.sleep(15)
        except Exception:
            time.sleep(30)


def start():
    threading.Thread(target=_run, daemon=True).start()
