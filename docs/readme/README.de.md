<div align="center">

<img src="../../release/flexcam-logo.png" width="96" alt="FlexCam" />

# FlexCam

**Verwandle dein Handy in eine PC-Webcam — über USB oder WLAN.**

[🇬🇧 English](../../README.md) · 🇩🇪 Deutsch

[Discord](https://discord.gg/EaNcFyCEqP) ·
[Instagram](https://instagram.com/null.rb) ·
[☕ Buy me a coffee](https://buymeacoffee.com/skydev)

</div>

---

## Was ist das

FlexCam überträgt die Kamera deines Android-Handys auf den PC und stellt sie als
**virtuelle Webcam** bereit, sodass jede App (Zoom, Teams, Discord, Browser,
OBS) sie als Kamera auswählen kann. Es funktioniert über **USB** (ADB) und
**WLAN** und wechselt automatisch, falls eine Verbindung abbricht.

- Hybrid **USB + WLAN** mit automatischem Failover
- **Verbindet sich automatisch**, sobald das Handy bereit ist
- **Live-Vorschau** auf Handy und PC
- **Vordere / hintere** Kamera, **automatisch Hoch-/Querformat**
- Streamt weiter bei **ausgeschaltetem Bildschirm**
- **WLAN-Zugangscode** — Fremde im Netzwerk können den Stream nicht sehen
- **10 Sprachen**, dunkle Oberfläche, Infobereich
- Läuft komplett auf deinem Gerät — **keine Daten verlassen deinen Computer**

## Treiber der virtuellen Kamera

FlexCam braucht eine virtuelle Kamera am PC. Du hast zwei Optionen:

- **Mitgelieferter Treiber (kein OBS nötig):** Wird beim ersten Start keine
  virtuelle Kamera gefunden, klicke in der App auf **„Virtuelle Kamera
  installieren"**. Registriert einmalig einen kleinen Open-Source-Treiber
  ([Unity Capture](https://github.com/schellingb/UnityCapture), MIT) mit
  einmaliger Admin-Abfrage.
- **OBS Studio:** Hast du bereits [OBS](https://obsproject.com/download), nutzt
  FlexCam dessen virtuelle Kamera automatisch.

## Schnellstart

1. **Handy:** `FlexCam.apk` installieren und App öffnen.
2. **PC:** **FlexCam-Windows.zip** entpacken und `FlexCam.exe` starten.
   - Erster Start: bei Aufforderung **„Virtuelle Kamera installieren"** (einmalig).
3. Verbindet sich per USB **automatisch**. Für WLAN die Handy-IP und den in der
   App angezeigten **Zugangscode** eingeben.
4. Wähle in deiner Video-App die Kamera **„OBS Virtual Camera"** (bzw.
   **„Unity Video Capture"** beim mitgelieferten Treiber).

> USB benötigt aktiviertes **USB-Debugging** (Entwickleroptionen). WLAN braucht
> kein Kabel.

## Aus Quellcode bauen

**Android (APK):**
```
cd android
gradlew assembleDebug
```
> Benötigt JDK 17.

**PC (Desktop-App):**
```
cd pc
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python webgui.py
```

Standalone-`.exe` mit PyInstaller (onedir) — siehe den Befehl im englischen README.

## Technik

- **Android:** Kotlin, CameraX, MJPEG-Server auf Port `8474`.
- **PC:** Python, pywebview-Oberfläche, `pyvirtualcam` → OBS oder Unity Capture.
- **Übertragung:** rohes TCP über `adb forward` (USB) oder die Handy-IP (WLAN).

## Lizenz

MIT — siehe [LICENSE](../../LICENSE).
