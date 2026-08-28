import numpy as np
import pyvirtualcam
from io import BytesIO
from PIL import Image


def jpeg_to_rgb(jpeg: bytes) -> np.ndarray:
    img = Image.open(BytesIO(jpeg)).convert("RGB")
    return np.asarray(img, dtype=np.uint8)


def fit_into_canvas(rgb: np.ndarray, out_w: int, out_h: int) -> np.ndarray:
    ih, iw = rgb.shape[:2]
    scale = min(out_w / iw, out_h / ih)
    nw = max(1, int(round(iw * scale)))
    nh = max(1, int(round(ih * scale)))
    resized = Image.fromarray(rgb).resize((nw, nh))
    canvas = np.zeros((out_h, out_w, 3), dtype=np.uint8)
    x = (out_w - nw) // 2
    y = (out_h - nh) // 2
    canvas[y:y + nh, x:x + nw] = np.asarray(resized, dtype=np.uint8)
    return canvas


class VirtualCamera:
    def __init__(self, width: int = 1280, height: int = 720, fps: int = 30):
        self._w = width
        self._h = height
        self._cam = None
        for backend in ("unitycapture", "obs"):
            try:
                self._cam = pyvirtualcam.Camera(
                    width=width, height=height, fps=fps, backend=backend
                )
                break
            except Exception:
                continue
        if self._cam is None:
            self._cam = pyvirtualcam.Camera(width=width, height=height, fps=fps)

    @property
    def device(self) -> str:
        return self._cam.device

    def send(self, rgb: np.ndarray) -> None:
        frame = fit_into_canvas(rgb, self._w, self._h)
        self._cam.send(frame)
        self._cam.sleep_until_next_frame()

    def close(self):
        if self._cam:
            self._cam.close()
