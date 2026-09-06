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
- **Mode distant (expérimental)** — utilisez votre téléphone depuis n'importe
  où, même en données mobiles, sans redirection de port ni compte
- **10 langues**, 6 thèmes, interface sombre, zone de notification
- USB et WiFi fonctionnent **entièrement sur votre appareil**

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
4. Dans votre app vidéo, choisissez la caméra **« FlexCam »** (ou
   **« OBS Virtual Camera »** si vous utilisez OBS).

> L'USB nécessite le **débogage USB** activé (options développeur). Le WiFi ne
> nécessite pas de câble.

## Connexion à distance (expérimental)

Le mode distant permet au téléphone d'atteindre votre PC depuis **n'importe
quel réseau** — autre WiFi, chez un ami, ou données mobiles. Rien à configurer :
aucune redirection de port, aucun réglage de box, aucun compte.

1. Sur le PC, ouvrez **Connexion à distance** et choisissez une qualité.
2. FlexCam ouvre un tunnel temporaire et affiche un **QR code**.
3. Sur le téléphone : **Connexion à distance → Scanner le QR code**.

**À savoir :**

- La vidéo transite par **Cloudflare**, qui termine le TLS et peut donc
  techniquement la voir. Ce n'est pas le cas en USB ni en WiFi.
- Cloudflare présente les Quick Tunnels comme destinés aux tests et au
  développement, sans garantie de disponibilité : d'où le statut expérimental.
- Attendez-vous à une **latence plus élevée** et à une vraie **consommation de
  données** ; chaque qualité affiche une estimation par heure.
- Chaque session génère une nouvelle adresse et un secret de 128 bits, jamais
  transmis ; après plusieurs échecs, l'écoute se coupe.
- Le mode distant est **désactivé par défaut**.

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

## Confidentialité

L'USB et le WiFi local gardent tout sur vos propres appareils.

Le mode distant fait exception : il fait transiter la vidéo par Cloudflare, car
c'est ce qui rend la connexion possible sans ouvrir de ports. Il ne fonctionne
que si vous l'activez.

## Licence

MIT — voir [LICENSE](../../LICENSE).
