<div align="center">

<img src="../../release/flexcam-logo.png" width="96" alt="FlexCam" />

# FlexCam

**Transformez votre téléphone en webcam PC — via USB ou WiFi.**

[🇬🇧 English](../../README.md) · 🇫🇷 Français

[Discord](https://discord.gg/EaNcFyCEqP) ·
[Instagram](https://instagram.com/null.rb) ·
[☕ Buy me a coffee](https://buymeacoffee.com/skydev)

</div>

---

## Qu'est-ce que c'est

FlexCam diffuse la caméra de votre téléphone Android vers votre PC et l'expose
comme une **webcam virtuelle**, afin que n'importe quelle app (Zoom, Teams,
Discord, navigateur, OBS) puisse la choisir comme caméra. Fonctionne via **USB**
(ADB) et **WiFi**, et bascule automatiquement si l'une tombe.

- Hybride **USB + WiFi** avec bascule automatique
- **Se connecte automatiquement** quand le téléphone est prêt
- **Aperçu en direct** sur le téléphone et le PC
- Caméra **avant / arrière**, **portrait/paysage automatique**
- Continue le flux **écran éteint**
- **Code d'accès WiFi** — les inconnus du réseau ne peuvent pas voir le flux
- **10 langues**, interface sombre, zone de notification
- Fonctionne entièrement sur votre appareil — **aucune donnée ne sort**

## Pilote de caméra virtuelle

FlexCam a besoin d'une caméra virtuelle sur le PC. Deux options :

- **Pilote inclus (sans OBS) :** au premier lancement, si aucune caméra
  virtuelle n'est trouvée, cliquez sur **« Installer la caméra virtuelle »**
  dans l'app. Il enregistre une fois un petit pilote open-source
  ([Unity Capture](https://github.com/schellingb/UnityCapture), MIT), avec une
  demande admin unique.
- **OBS Studio :** si vous avez déjà [OBS](https://obsproject.com/download),
  FlexCam utilise sa caméra virtuelle automatiquement.

## Démarrage rapide

1. **Téléphone :** installez `FlexCam.apk` et ouvrez l'app.
2. **PC :** décompressez **FlexCam-Windows.zip** et lancez `FlexCam.exe`.
   - Premier lancement : si demandé, cliquez sur **« Installer la caméra
     virtuelle »** (une fois).
3. Se connecte en USB **automatiquement**. Pour le WiFi, saisissez l'IP du
   téléphone et le **code d'accès** affiché dans l'app.
4. Dans votre app vidéo, choisissez la caméra **« OBS Virtual Camera »** (ou
   **« Unity Video Capture »** avec le pilote inclus).

> L'USB nécessite le **débogage USB** activé (options développeur). Le WiFi ne
> nécessite pas de câble.

## Compiler depuis les sources

**Android (APK):**
```
cd android
gradlew assembleDebug
```
> Nécessite JDK 17.

**PC (application de bureau):**
```
cd pc
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python webgui.py
```

`.exe` autonome avec PyInstaller (onedir) — voir la commande dans le README anglais.

## Technique

- **Android :** Kotlin, CameraX, serveur MJPEG sur le port `8474`.
- **PC :** Python, interface pywebview, `pyvirtualcam` → OBS ou Unity Capture.
- **Transport :** TCP brut via `adb forward` (USB) ou l'IP du téléphone (WiFi).

## Licence

MIT — voir [LICENSE](../../LICENSE).
