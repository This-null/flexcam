import functools

import numpy as np
from PIL import Image, ImageEnhance, ImageOps

KEYS = ("brightness", "contrast", "saturation", "warmth", "shadows", "sharpness")

PRESETS = {
    "original": {},
    "night": {"brightness": 18, "shadows": 55, "contrast": 10, "saturation": 8, "sharpness": 10},
    "bright": {"brightness": 20, "contrast": 5, "saturation": 12},
    "studio": {"brightness": 10, "contrast": 14, "sharpness": 25, "shadows": 20, "saturation": 6, "warmth": 4},
    "warm": {"warmth": 45, "saturation": 10, "brightness": 4},
    "cool": {"warmth": -40, "contrast": 6, "saturation": -4},
    "cinema": {"contrast": 28, "saturation": -14, "shadows": -10, "warmth": 10, "brightness": -4},
    "glow": {"brightness": 8, "contrast": -8, "sharpness": -35, "saturation": 8},
}


def normalize(params):
    p = {k: 0 for k in KEYS}
    p["mirror"] = False
    for k in KEYS:
        try:
            p[k] = max(-100, min(100, int(params.get(k, 0))))
        except (TypeError, ValueError):
            p[k] = 0
    p["mirror"] = bool(params.get("mirror", False))
    return p


def preset(name):
    p = normalize(PRESETS.get(name, {}))
    return p


def is_identity(p):
    return not p.get("mirror") and all(not p.get(k) for k in KEYS)


@functools.lru_cache(maxsize=64)
def _lut(shadows, warmth, brightness, contrast):
    gamma = 1.0 / (1.0 + 0.01 * shadows) if shadows >= 0 else 1.0 - 0.01 * shadows
    gains = (1.0 + 0.2 * warmth / 100.0, 1.0, 1.0 - 0.2 * warmth / 100.0)
    bright = 1.0 + brightness / 100.0
    punch = 1.0 + contrast / 100.0
    x = np.arange(256, dtype=np.float32) / 255.0
    base = np.power(x, gamma)
    out = []
    for gain in gains:
        v = (base * gain * bright - 0.5) * punch + 0.5
        out.extend(np.clip(v * 255.0 + 0.5, 0, 255).astype(np.uint8).tolist())
    return tuple(out)


def apply(rgb, p):
    if is_identity(p):
        return rgb
    img = Image.fromarray(rgb)
    if p["mirror"]:
        img = ImageOps.mirror(img)
    if p["shadows"] or p["warmth"] or p["brightness"] or p["contrast"]:
        img = img.point(list(_lut(p["shadows"], p["warmth"], p["brightness"], p["contrast"])))
    if p["saturation"]:
        img = ImageEnhance.Color(img).enhance(1.0 + p["saturation"] / 100.0)
    if p["sharpness"]:
        factor = 1.0 + p["sharpness"] / 50.0 if p["sharpness"] > 0 else 1.0 + p["sharpness"] / 100.0
        img = ImageEnhance.Sharpness(img).enhance(max(0.0, factor))
    return np.asarray(img, dtype=np.uint8)


def selfcheck():
    rng = np.random.default_rng(7)
    h, w = 720, 1280
    grad = np.linspace(20, 200, w, dtype=np.float32)[None, :, None].repeat(h, 0).repeat(3, 2)
    frame = np.clip(grad + rng.normal(0, 6, (h, w, 3)), 0, 255).astype(np.uint8)
    luma = lambda a: float(a.mean())

    assert apply(frame, preset("original")) is frame
    assert luma(apply(frame, normalize({"brightness": 40}))) > luma(frame) + 5
    assert luma(apply(frame, preset("night"))) > luma(frame) + 8
    assert luma(apply(frame, normalize({"brightness": -40}))) < luma(frame) - 5
    assert np.array_equal(apply(frame, normalize({"mirror": True})), frame[:, ::-1])
    gray = apply(frame, normalize({"saturation": -100})).astype(np.int32)
    assert np.abs(gray[..., 0] - gray[..., 1]).max() <= 2 and np.abs(gray[..., 1] - gray[..., 2]).max() <= 2
    warm = apply(frame, normalize({"warmth": 80}))
    assert warm[..., 0].mean() > frame[..., 0].mean() and warm[..., 2].mean() < frame[..., 2].mean()
    cool = apply(frame, normalize({"warmth": -80}))
    assert cool[..., 2].mean() > frame[..., 2].mean() and cool[..., 0].mean() < frame[..., 0].mean()
    assert apply(frame, normalize({"contrast": 60})).std() > frame.std()
    soft = apply(frame, normalize({"sharpness": -60}))
    assert float(np.abs(np.diff(soft.astype(np.int32), axis=1)).mean()) < float(np.abs(np.diff(frame.astype(np.int32), axis=1)).mean())
    assert normalize({"brightness": "x", "contrast": 999})["contrast"] == 100
    assert normalize({"brightness": "x"})["brightness"] == 0
    return True


if __name__ == "__main__":
    import time
    print("selfcheck:", selfcheck())
    f = (np.random.default_rng(1).random((720, 1280, 3)) * 255).astype(np.uint8)
    g = f[:480, :640].copy()
    print(f"{'on ayar':9s} {'640x480':>10s} {'1280x720':>10s}")
    for name in PRESETS:
        p = preset(name)
        row = []
        for fr in (g, f):
            apply(fr, p)
            t = time.perf_counter()
            for _ in range(20):
                apply(fr, p)
            row.append((time.perf_counter() - t) / 20 * 1000)
        print(f"{name:9s} {row[0]:8.1f}ms {row[1]:8.1f}ms")
