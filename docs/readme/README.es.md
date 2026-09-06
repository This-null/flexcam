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
- **Modo remoto (experimental)** — usa el teléfono desde cualquier lugar,
  incluso con datos móviles, sin abrir puertos y sin cuenta
- **10 idiomas**, 6 temas, interfaz oscura, bandeja
- USB y WiFi funcionan **totalmente en tu dispositivo**

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
4. En tu app de video, elige la cámara **"FlexCam"** (o
   **"OBS Virtual Camera"** si usas OBS).

> USB necesita la **depuración USB** activada (opciones de desarrollador). WiFi
> no necesita cable.

## Conexión remota (experimental)

El modo remoto permite que el teléfono llegue a tu PC desde **cualquier red**:
otro WiFi, casa de un amigo o datos móviles. No hay nada que configurar: sin
apertura de puertos, sin ajustes del router y sin cuenta.

1. En el PC, abre **Conexión remota** y elige una calidad.
2. FlexCam abre un túnel temporal y muestra un **código QR**.
3. En el teléfono, pulsa **Conectar en remoto → Escanear código QR**.

**Lo que debes saber:**

- El vídeo pasa por **Cloudflare**, que termina el TLS y técnicamente puede
  verlo. En USB y WiFi esto no ocurre.
- Cloudflare indica que los Quick Tunnels son para pruebas y desarrollo, sin
  garantía de disponibilidad; por eso la función es experimental.
- Habrá **más latencia** y un **consumo de datos real**; cada calidad muestra
  una estimación por hora.
- Cada sesión genera una dirección nueva y un secreto de 128 bits que nunca se
  transmite; tras varios intentos fallidos todo se detiene.
- El modo remoto está **desactivado por defecto**.

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

## Privacidad

USB y WiFi local mantienen todo en tus propios dispositivos.

El modo remoto es la excepción: envía el vídeo por la red de Cloudflare, porque
es lo que hace posible la conexión sin abrir puertos. Solo funciona si lo
activas.

## Licencia

MIT — ver [LICENSE](../../LICENSE).
