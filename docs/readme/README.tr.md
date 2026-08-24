<div align="center">

<img src="../../release/flexcam-logo.png" width="96" alt="FlexCam" />

# FlexCam

**Telefonunu USB veya WiFi ile PC webcam'ine çevir.**

[🇬🇧 English](../../README.md) · 🇹🇷 Türkçe

[Discord](https://discord.gg/EaNcFyCEqP) ·
[Instagram](https://instagram.com/null.rb) ·
[☕ Bir kahve ısmarla](https://buymeacoffee.com/skydev)

</div>

---

## Nedir

FlexCam, Android telefonunun kamerasını PC'ne aktarır ve bir **sanal webcam**
olarak gösterir; böylece herhangi bir uygulama (Zoom, Teams, Discord, tarayıcı,
OBS) onu kamera olarak seçebilir. **USB** (ADB) ve **WiFi** üzerinden çalışır,
biri koparsa otomatik olarak diğerine geçer.

- Hibrit **USB + WiFi**, otomatik yük devretme
- Telefon hazır olunca **otomatik bağlanır** — elle işlem yok
- Telefonda ve PC'de **canlı önizleme**
- **Ön / arka** kamera geçişi, **otomatik dik/yatay**
- **Ekran kapalıyken** de yayın sürer
- **WiFi erişim kodu** — ağdaki yabancılar yayınını izleyemez
- **10 dil**, koyu arayüz, tepsi desteği
- Tamamen cihazında çalışır — **hiçbir veri dışarı gönderilmez**

## Sanal kamera sürücüsü

FlexCam'in PC'de bir sanal kameraya ihtiyacı var. İki seçeneğin var:

- **Gömülü sürücü (OBS gerekmez):** İlk açılışta sanal kamera bulunamazsa,
  uygulamadaki **"Sanal kamera kur"** düğmesine tıkla. Küçük, açık kaynak bir
  sürücüyü ([Unity Capture](https://github.com/schellingb/UnityCapture), MIT)
  tek seferlik yönetici onayıyla kaydeder.
- **OBS Studio:** Zaten [OBS](https://obsproject.com/download) kuruluysa FlexCam
  onun sanal kamerasını otomatik kullanır.

## Hızlı başlangıç

1. **Telefon:** `FlexCam.apk`'yı kur ve uygulamayı aç.
2. **PC:** **FlexCam-Windows.zip**'i aç ve `FlexCam.exe`'yi çalıştır.
   - İlk açılış: istenirse **"Sanal kamera kur"**a tıkla (tek seferlik).
3. USB üzerinden **otomatik bağlanır**. WiFi için telefonun IP'sini ve
   uygulamada görünen **erişim kodunu** yaz.
4. Video uygulamanda kamera olarak **"OBS Virtual Camera"** (gömülü sürücü
   kullandıysan **"Unity Video Capture"**) seç.

> USB için **USB hata ayıklama** açık olmalı (Geliştirici Seçenekleri).
> WiFi kablo istemez.

## Kaynaktan derleme

**Android (APK):**
```
cd android
gradlew assembleDebug
```
> JDK 17 gerekir.

**PC (masaüstü uygulaması):**
```
cd pc
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python webgui.py
```

Bağımsız `.exe` paketlemek (PyInstaller, onedir): İngilizce README'deki komuta
bak.

## Teknik

- **Android:** Kotlin, CameraX, `8474` portunda MJPEG sunucu.
- **PC:** Python, pywebview arayüz, `pyvirtualcam` → OBS veya Unity Capture.
- **Aktarım:** `adb forward` (USB) ya da telefonun IP'si (WiFi) üzerinden ham TCP.

## Lisans

MIT — bkz. [LICENSE](../../LICENSE).
