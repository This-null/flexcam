<div align="center">

<img src="../../release/flexcam-logo.png" width="96" alt="FlexCam" />

# FlexCam

**Convierte tu teléfono en una webcam de PC — por USB o WiFi.**

[🇬🇧 English](../../README.md) · 🇪🇸 Español

[Discord](https://discord.gg/EaNcFyCEqP) ·
[Instagram](https://instagram.com/null.rb) ·
[☕ Buy me a coffee](https://buymeacoffee.com/skydev)

</div>

---

## Qué es

FlexCam transmite la cámara de tu teléfono Android al PC y la expone como una
**webcam virtual**, para que cualquier app (Zoom, Teams, Discord, navegador,
OBS) pueda elegirla como cámara. Funciona por **USB** (ADB) y **WiFi**, y cambia
automáticamente si una se cae.

- Híbrido **USB + WiFi** con conmutación automática
- **Se conecta automáticamente** cuando el teléfono está listo
- **Vista previa en vivo** en el teléfono y el PC
- Cámara **frontal / trasera**, **vertical/horizontal automático**
- Sigue transmitiendo con la **pantalla apagada**
- **Código de acceso WiFi** — los desconocidos de tu red no ven la transmisión
- **10 idiomas**, interfaz oscura, bandeja
- Funciona totalmente en tu dispositivo — **ningún dato sale de tu ordenador**

## Controlador de cámara virtual

FlexCam necesita una cámara virtual en el PC. Tienes dos opciones:

- **Controlador incluido (sin OBS):** en el primer uso, si no se encuentra una
  cámara virtual, haz clic en **"Instalar cámara virtual"** en la app. Registra
  una vez un pequeño controlador de código abierto
  ([Unity Capture](https://github.com/schellingb/UnityCapture), MIT), con una
  solicitud de administrador única.
- **OBS Studio:** si ya tienes [OBS](https://obsproject.com/download), FlexCam
  usa su cámara virtual automáticamente.

## Inicio rápido

1. **Teléfono:** instala `FlexCam.apk` y abre la app.
2. **PC:** descomprime **FlexCam-Windows.zip** y ejecuta `FlexCam.exe`.
   - Primer uso: si se pide, haz clic en **"Instalar cámara virtual"** (una vez).
3. Se conecta por USB **automáticamente**. Para WiFi, escribe la IP del teléfono
   y el **código de acceso** que muestra la app.
4. En tu app de video, elige la cámara **"OBS Virtual Camera"** (o
   **"Unity Video Capture"** con el controlador incluido).

> USB necesita la **depuración USB** activada (opciones de desarrollador). WiFi
> no necesita cable.

## Compilar desde el código

**Android (APK):**
```
cd android
gradlew assembleDebug
```
> Requiere JDK 17.

**PC (app de escritorio):**
```
cd pc
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python webgui.py
```

`.exe` independiente con PyInstaller (onedir) — mira el comando en el README en inglés.

## Tecnología

- **Android:** Kotlin, CameraX, servidor MJPEG en el puerto `8474`.
- **PC:** Python, interfaz pywebview, `pyvirtualcam` → OBS o Unity Capture.
- **Transporte:** TCP puro vía `adb forward` (USB) o la IP del teléfono (WiFi).

## Licencia

MIT — ver [LICENSE](../../LICENSE).
