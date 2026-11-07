import threading

import config

_stop = threading.Event()
_thread = None


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


def _update(rpc, start):
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


def _run():
    import time
    try:
        from pypresence import Presence
    except Exception:
        return
    if not config.DISCORD_CLIENT_ID:
        return
    while not _stop.is_set():
        rpc = None
        try:
            rpc = Presence(config.DISCORD_CLIENT_ID)
            rpc.connect()
            _update(rpc, int(time.time()))
            while not _stop.wait(15):
                pass
        except Exception:
            _stop.wait(30)
        finally:
            if rpc is not None:
                try:
                    rpc.clear()
                    rpc.close()
                except Exception:
                    pass


def start():
    global _thread
    if _thread is not None and _thread.is_alive():
        return
    _stop.clear()
    _thread = threading.Thread(target=_run, daemon=True)
    _thread.start()


def stop():
    _stop.set()
