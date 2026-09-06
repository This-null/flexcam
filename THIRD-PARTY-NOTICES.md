# Third-party notices

FlexCam's own source code is licensed under the MIT License (see [LICENSE](LICENSE)).

The prebuilt Windows application distributed on the releases page bundles the
third-party components listed below. Because it includes **pyvirtualcam**,
which is licensed under the GNU General Public License v2.0, the bundled
Windows build as a whole is distributed under the terms of the **GPL-2.0**.
The complete corresponding source code is available at
https://github.com/This-null/flexcam — the MIT licensing of FlexCam's own
source is unaffected.

## Desktop application

| Component | Version | License |
| --- | --- | --- |
| [pyvirtualcam](https://github.com/letmaik/pyvirtualcam) | 0.15.0 | GPL-2.0 |
| [pystray](https://github.com/moses-palmer/pystray) | 0.19.5 | LGPL-3.0 |
| [pywebview](https://github.com/r0x0r/pywebview) | 6.2.1 | BSD-3-Clause |
| [Pillow](https://github.com/python-pillow/Pillow) | 12.3.0 | MIT-CMU |
| [NumPy](https://github.com/numpy/numpy) | 2.5.2 | BSD-3-Clause |
| [pypresence](https://github.com/qwertyquerty/pypresence) | 4.6.2 | MIT |
| [websockets](https://github.com/python-websockets/websockets) | 17.1 | BSD-3-Clause |
| [qrcode](https://github.com/lincolnloop/python-qrcode) | 8.2 | BSD-3-Clause |
| [cloudflared](https://github.com/cloudflare/cloudflared) | 2026.8.3 | Apache-2.0 |
| [Unity Capture](https://github.com/schellingb/UnityCapture) filter | — | MIT |
| Android Debug Bridge (`adb`) | — | Android SDK terms |

## Android application

| Component | Version | License |
| --- | --- | --- |
| [AndroidX CameraX](https://developer.android.com/jetpack/androidx/releases/camera) | 1.4.1 | Apache-2.0 |
| [AndroidX AppCompat, Core-KTX, Activity, Lifecycle](https://developer.android.com/jetpack) | — | Apache-2.0 |
| [OkHttp](https://github.com/square/okhttp) | 4.12.0 | Apache-2.0 |
| [ZXing Android Embedded](https://github.com/journeyapps/zxing-android-embedded) | 4.3.0 | Apache-2.0 |
| [ZXing core](https://github.com/zxing/zxing) | — | Apache-2.0 |

## Notes on specific components

Unity Capture is Copyright (c) 2018 Bernhard Schelling, based on UnityCam,
Copyright (c) 2016 MHD Yamen Saraiji. Its full license text ships with the
application in `virtualcam/LICENSE-UnityCapture.txt`.

`cloudflared` is bundled to provide the optional remote-connection mode. It is
started only while that mode is running and is terminated when it stops. See
the privacy note below.

`adb.exe` and its DLLs are part of the Android SDK Platform-Tools, distributed
by Google under the Android Software Development Kit License Agreement.

## Privacy

USB and local WiFi modes keep everything on your own devices: the video never
leaves your machine or your network.

**Remote mode is different.** It opens a Cloudflare Quick Tunnel so a phone on
any network can reach the desktop app. Video therefore travels through
Cloudflare's network, which terminates TLS and can technically observe it.
Remote mode is off by default and must be started explicitly. Cloudflare
documents Quick Tunnels as intended for testing and development, with no
uptime guarantee, which is why the feature is labelled Experimental.

The connection itself is authenticated with a 128-bit secret using an
HMAC-SHA256 challenge-response; the secret is never transmitted, is regenerated
for every session, and repeated failed attempts stop the listener.
