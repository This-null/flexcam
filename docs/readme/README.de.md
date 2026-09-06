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
- **Fernmodus (experimentell)** — nutze dein Handy von überall, auch mobil;
  ohne Portfreigabe und ohne Konto
- **10 Sprachen**, 6 Themes, dunkle Oberfläche, Infobereich
- USB und WLAN laufen **komplett auf deinem Gerät**

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
4. Wähle in deiner Video-App die Kamera **„FlexCam“** (oder
   **„OBS Virtual Camera“**, falls du OBS nutzt).

> USB benötigt aktiviertes **USB-Debugging** (Entwickleroptionen). WLAN braucht
> kein Kabel.

## Fernverbindung (experimentell)

Der Fernmodus lässt das Handy deinen PC aus **jedem Netz** erreichen — anderes
WLAN, bei Freunden oder mobil. Es gibt nichts einzurichten: keine Portfreigabe,
keine Router-Einstellungen, kein Konto.

1. Am PC **Fernverbindung** öffnen und eine Qualität wählen.
2. FlexCam öffnet einen temporären Tunnel und zeigt einen **QR-Code**.
3. Am Handy auf **Fernverbindung → QR-Code scannen** tippen.

**Wichtig zu wissen:**

- Das Video läuft über **Cloudflare**, wo TLS endet und es technisch einsehbar
  ist. Bei USB und WLAN passiert das nicht.
- Cloudflare bezeichnet Quick Tunnels als für Test und Entwicklung gedacht,
  ohne Verfügbarkeitsgarantie — deshalb gilt die Funktion als experimentell.
- Rechne mit **höherer Latenz** und echtem **Datenverbrauch**; die
  Qualitätsstufen zeigen eine Schätzung pro Stunde.
- Jede Sitzung erzeugt eine neue Adresse und ein neues 128-Bit-Geheimnis. Es
  wird nie übertragen; nach mehreren Fehlversuchen schaltet sich alles ab.
- Der Fernmodus ist **standardmäßig aus**.

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

## Datenschutz

USB und lokales WLAN behalten alles auf deinen eigenen Geräten.

Der Fernmodus ist die Ausnahme: Er leitet das Video bewusst über Cloudflare,
denn nur so gelingt eine Verbindung ohne offene Ports. Er läuft nur, wenn du
ihn einschaltest.

## Lizenz

MIT — siehe [LICENSE](../../LICENSE).
