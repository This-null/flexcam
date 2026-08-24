<div align="center">

<img src="release/flexcam-logo.png" width="96" alt="FlexCam" />

# FlexCam

**Turn your phone into a PC webcam — over USB or WiFi.**

🇬🇧 English ·
[🇹🇷 Türkçe](docs/readme/README.tr.md) ·
[🇩🇪 Deutsch](docs/readme/README.de.md) ·
[🇫🇷 Français](docs/readme/README.fr.md) ·
[🇵🇹 Português](docs/readme/README.pt.md) ·
[🇪🇸 Español](docs/readme/README.es.md) ·
[🇦🇿 Azərbaycan](docs/readme/README.az.md) ·
[🇨🇳 中文](docs/readme/README.zh.md) ·
[🇯🇵 日本語](docs/readme/README.ja.md) ·
[🇮🇳 हिन्दी](docs/readme/README.hi.md)

[Discord](https://discord.gg/EaNcFyCEqP) ·
[Instagram](https://instagram.com/null.rb) ·
[☕ Buy me a coffee](https://buymeacoffee.com/skydev)

</div>

---

## What it is

FlexCam streams your Android phone's camera to your PC and exposes it as a
**virtual webcam**, so any app (Zoom, Teams, Discord, your browser, OBS) can
pick it as a camera. It works over **USB** (via ADB) and **WiFi**, and switches
between them automatically if one drops.

- Hybrid **USB + WiFi** with automatic failover
- **Auto-connects** when your phone is ready — no manual steps
- **Live preview** on both phone and PC
- **Front / back** camera switch, **auto portrait/landscape**
- Keeps streaming with the **screen off**
- **WiFi access code** — strangers on your network can't view the stream
- **10 languages**, dark UI, tray support
- Runs fully on your device — **no data ever leaves your computer**

## Virtual camera driver

FlexCam needs a virtual camera on the PC. You have two options:

- **Bundled driver (no OBS needed):** on first run, if no virtual camera is
  found, click **"Install virtual camera"** in the app. It registers a small
  open-source driver ([Unity Capture](https://github.com/schellingb/UnityCapture),
  MIT) once, with a one-time admin prompt.
- **OBS Studio:** if you already have [OBS](https://obsproject.com/download),
  FlexCam uses its Virtual Camera automatically.

## Quick start

1. **Phone:** install `FlexCam.apk` and open the app.
2. **PC:** unzip **FlexCam-Windows.zip** and run `FlexCam.exe`.
   - First run: if prompted, click **"Install virtual camera"** (one-time).
3. It **auto-connects** over USB. For WiFi, type the phone's IP and the
   **access code** shown in the app.
4. In your video app, pick the camera **"OBS Virtual Camera"** (or
   **"Unity Video Capture"** if you used the bundled driver).

> USB needs **USB debugging** enabled (Developer Options). WiFi needs no cable.

## Build from source

**Android (APK):**
```
cd android
gradlew assembleDebug
```
> Requires JDK 17.

**PC (desktop app):**
```
cd pc
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python webgui.py
```

Package a standalone `.exe` with PyInstaller (onedir):
```
.venv\Scripts\python -m PyInstaller --noconfirm --onedir --windowed --name FlexCam ^
  --add-data "web;web" --add-data "flexcam-logo.png;." --add-data "FlexCam.apk;." ^
  --add-data "adb;adb" --add-data "virtualcam;virtualcam" ^
  --collect-all pyvirtualcam --collect-all pystray --collect-all webview ^
  --collect-all pythonnet --collect-all clr_loader --collect-all pypresence webgui.py
```

## Tech

- **Android:** Kotlin, CameraX, an MJPEG server on port `8474`.
- **PC:** Python, pywebview UI, `pyvirtualcam` → OBS or Unity Capture.
- **Transport:** raw TCP over `adb forward` (USB) or the phone's IP (WiFi).

## License

MIT — see [LICENSE](LICENSE).
