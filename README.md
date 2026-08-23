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

> [!CAUTION]
> **FlexCam requires [OBS Studio](https://obsproject.com/download) to be installed.**
> It uses the OBS Virtual Camera driver to expose your phone as a webcam.
> Install OBS once — you don't need to keep it open.

---

## What it is

FlexCam streams your Android phone's camera to your PC and exposes it as
**"OBS Virtual Camera"**, so any app (Zoom, Teams, Discord, your browser, OBS)
can pick it as a webcam. It works over **USB** (via ADB) and **WiFi**, and
switches between them automatically if one drops.

- Hybrid **USB + WiFi** with automatic failover
- **Auto-connects** when your phone is ready — no manual steps
- **Front / back** camera switch
- **Auto portrait/landscape** (follows the phone's rotation)
- Keeps streaming with the **screen off**
- **10 languages**, dark UI, tray support
- Runs fully on your device — **no data leaves your computer**

## Quick start

1. Install **OBS Studio** (once).
2. On the phone: install `release/FlexCam.apk` and open the app.
3. On the PC: run **FlexCam** and it auto-connects.
4. In your video app, choose the camera **"OBS Virtual Camera"**.

USB needs **USB debugging** enabled (Developer Options). WiFi needs no cable —
just type the IP the phone app shows.

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

## Tech

- **Android:** Kotlin, CameraX, MJPEG server on port `8474`.
- **PC:** Python, pywebview UI, `pyvirtualcam` → OBS Virtual Camera.
- **Transport:** raw TCP over `adb forward` (USB) or the phone's IP (WiFi).

## License

MIT — see [LICENSE](LICENSE).
