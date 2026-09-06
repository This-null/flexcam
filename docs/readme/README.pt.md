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
- **Modo remoto (experimental)** — use o telefone de qualquer lugar, mesmo com
  dados móveis, sem redirecionamento de portas e sem conta
- **10 idiomas**, 6 temas, interface escura, bandeja
- USB e WiFi rodam **totalmente no seu dispositivo**

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
4. No seu app de vídeo, escolha a câmera **"FlexCam"** (ou
   **"OBS Virtual Camera"** se você usa OBS).

> USB precisa de **depuração USB** ativada (Opções do desenvolvedor). WiFi não
> precisa de cabo.

## Conexão remota (experimental)

O modo remoto permite que o telefone alcance o PC a partir de **qualquer
rede** — outro WiFi, a casa de um amigo ou dados móveis. Não há nada a
configurar: sem redirecionamento de portas, sem ajustes de roteador, sem conta.

1. No PC, abra **Conexão remota** e escolha uma qualidade.
2. O FlexCam abre um túnel temporário e mostra um **QR code**.
3. No telefone, toque em **Conectar remotamente → Escanear QR code**.

**O que você deve saber:**

- O vídeo passa pela **Cloudflare**, que termina o TLS e pode tecnicamente
  vê-lo. Isso não acontece nos modos USB e WiFi.
- A Cloudflare documenta os Quick Tunnels como voltados a teste e
  desenvolvimento, sem garantia de disponibilidade — daí o rótulo experimental.
- Espere **latência maior** e **consumo real de dados**; cada qualidade mostra
  uma estimativa por hora.
- Cada sessão gera um novo endereço e um segredo de 128 bits, nunca
  transmitido; após várias tentativas erradas tudo é encerrado.
- O modo remoto vem **desligado por padrão**.

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

## Privacidade

USB e WiFi local mantêm tudo nos seus próprios dispositivos.

O modo remoto é a exceção: ele encaminha o vídeo pela rede da Cloudflare, pois
é isso que torna a conexão possível sem abrir portas. Só funciona se você
ligá-lo.

## Licença

MIT — veja [LICENSE](../../LICENSE).
