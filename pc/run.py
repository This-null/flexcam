import sys
import time

from engine import FlexCamEngine


def main():
    ip = sys.argv[1] if len(sys.argv) > 1 else None
    engine = FlexCamEngine(
        wifi_ip=ip,
        on_status=lambda state, src, detail: print(f"[{state}] {detail}"),
    )
    engine.start()
    try:
        while engine.is_running():
            time.sleep(0.3)
    except KeyboardInterrupt:
        engine.stop()
        time.sleep(0.5)
    return 0


if __name__ == "__main__":
    sys.exit(main())
