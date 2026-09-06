<div align="center">

<img src="release/flexcam-logo.png" width="96" alt="FlexCam" />

# FlexCam

**Turn your phone into a PC webcam — over USB, WiFi, or from anywhere.**

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
pick it as a camera. It works over **USB** (via ADB) and **WiFi**, switching between them
automatically if one drops, and can also connect from **any network** —
including mobile data — with the experimental remote mode.

- Hybrid **USB + WiFi** with automatic failover
- **Auto-connects** when your phone is ready — no manual steps
- **Live preview** on both phone and PC
- **Front / back** camera switch, **auto portrait/landscape**
- Keeps streaming with the **screen off**
- **WiFi access code** — strangers on your network can't view the stream
- **Remote mode (experimental)** — use your phone from anywhere, even on
  mobile data, with no port forwarding and no account
- **10 languages**, 6 themes, dark UI, tray support
- USB and WiFi run **fully on your device**

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
4. In your video app, pick the camera named **"FlexCam"** (or
   **"OBS Virtual Camera"** if you rely on OBS instead).

> USB needs **USB debugging** enabled (Developer Options). WiFi needs no cable.

## Remote connection (experimental)

Remote mode lets the phone reach your PC from **any network** — a different
WiFi, a friend's house, or mobile data. There is nothing to configure: no port
forwarding, no router settings, no account.

1. On the PC, open **Remote connection** and pick a quality preset.
2. FlexCam opens a temporary tunnel and shows a **QR code**.
3. On the phone, tap **Connect remotely → Scan QR code**.

The phone then streams to your PC and the virtual camera works as usual.

**What you should know:**

- Video is relayed through **Cloudflare**, which terminates TLS and can
  technically see it. USB and WiFi modes do not do this.
- The tunnel uses Cloudflare Quick Tunnels, which Cloudflare documents as
  intended for testing and development, with no uptime guarantee. That is why
  the feature is marked experimental.
- Expect **higher latency** than on a local network, and real **mobile data
  use** — the quality presets show an estimate per hour.
- Each session generates a new address and a new 128-bit secret. The secret is
  never sent over the wire, and repeated wrong attempts shut the listener down.
- Remote mode is **off by default** and stops when you close it.

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

## Privacy

USB and local WiFi keep everything on your own devices — the video never leaves
your machine or your network.

Remote mode is the exception: it routes video through Cloudflare's network by
design, because that is what makes a connection possible without opening ports.
It is off unless you turn it on.

## License

FlexCam's own source code is MIT — see [LICENSE](LICENSE).

The prebuilt Windows download bundles [pyvirtualcam](https://github.com/letmaik/pyvirtualcam) (GPL-2.0), so that build is distributed under the GPL-2.0 as a whole. See [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md) for the full list.
