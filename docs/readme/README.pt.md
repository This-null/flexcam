<div align="center">

<img src="../../release/flexcam-logo.png" width="96" alt="FlexCam" />

# FlexCam

**Transforme seu telefone numa webcam de PC — via USB ou WiFi.**

[🇬🇧 English](../../README.md) · 🇵🇹 Português

[Discord](https://discord.gg/EaNcFyCEqP) ·
[Instagram](https://instagram.com/null.rb) ·
[☕ Buy me a coffee](https://buymeacoffee.com/skydev)

</div>

---

## O que é

O FlexCam transmite a câmera do seu telefone Android para o PC e a expõe como uma
**webcam virtual**, para que qualquer app (Zoom, Teams, Discord, navegador, OBS)
possa escolhê-la como câmera. Funciona via **USB** (ADB) e **WiFi**, e alterna
automaticamente se uma cair.

- Híbrido **USB + WiFi** com troca automática
- **Conecta automaticamente** quando o telefone está pronto
- **Pré-visualização ao vivo** no telefone e no PC
- Câmera **frontal / traseira**, **retrato/paisagem automático**
- Continua transmitindo com a **tela desligada**
- **Código de acesso WiFi** — estranhos na sua rede não veem a transmissão
- **10 idiomas**, interface escura, bandeja
- Roda totalmente no seu dispositivo — **nenhum dado sai do seu computador**

## Driver de câmera virtual

O FlexCam precisa de uma câmera virtual no PC. Você tem duas opções:

- **Driver incluído (sem OBS):** no primeiro uso, se nenhuma câmera virtual for
  encontrada, clique em **"Instalar câmera virtual"** no app. Ele registra uma
  vez um pequeno driver de código aberto
  ([Unity Capture](https://github.com/schellingb/UnityCapture), MIT), com um
  pedido de administrador único.
- **OBS Studio:** se você já tem o [OBS](https://obsproject.com/download), o
  FlexCam usa a câmera virtual dele automaticamente.

## Início rápido

1. **Telefone:** instale `FlexCam.apk` e abra o app.
2. **PC:** extraia **FlexCam-Windows.zip** e execute `FlexCam.exe`.
   - Primeiro uso: se solicitado, clique em **"Instalar câmera virtual"** (uma vez).
3. Conecta por USB **automaticamente**. Para WiFi, digite o IP do telefone e o
   **código de acesso** mostrado no app.
4. No seu app de vídeo, escolha a câmera **"OBS Virtual Camera"** (ou
   **"Unity Video Capture"** com o driver incluído).

> USB precisa de **depuração USB** ativada (Opções do desenvolvedor). WiFi não
> precisa de cabo.

## Compilar do código-fonte

**Android (APK):**
```
cd android
gradlew assembleDebug
```
> Requer JDK 17.

**PC (app de desktop):**
```
cd pc
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python webgui.py
```

`.exe` independente com PyInstaller (onedir) — veja o comando no README em inglês.

## Tecnologia

- **Android:** Kotlin, CameraX, servidor MJPEG na porta `8474`.
- **PC:** Python, interface pywebview, `pyvirtualcam` → OBS ou Unity Capture.
- **Transporte:** TCP puro via `adb forward` (USB) ou o IP do telefone (WiFi).

## Licença

MIT — veja [LICENSE](../../LICENSE).
