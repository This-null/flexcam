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
- **Uzak mod (deneysel)** — telefonunu her yerden, mobil veriyle bile kullan;
  port yönlendirme ve hesap gerekmez
- **10 dil**, 6 tema, koyu arayüz, tepsi desteği
- USB ve WiFi **tamamen cihazında** çalışır

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
4. Video uygulamanda kamera olarak **"FlexCam"** seç (OBS'ye güveniyorsan
   **"OBS Virtual Camera"**).

> USB için **USB hata ayıklama** açık olmalı (Geliştirici Seçenekleri).
> WiFi kablo istemez.

## Uzaktan bağlantı (deneysel)

Uzak mod, telefonun PC'ne **herhangi bir ağdan** ulaşmasını sağlar — başka bir
WiFi, arkadaşının evi ya da mobil veri. Ayar yapmana gerek yok: port
yönlendirme yok, modem ayarı yok, hesap yok.

1. PC'de **Uzaktan bağlantı**'yı aç ve bir kalite seç.
2. FlexCam geçici bir tünel açar ve bir **QR kod** gösterir.
3. Telefonda **Uzaktan bağlan → QR kodu okut**'a dokun.

Telefon PC'ne yayın yapmaya başlar, sanal kamera her zamanki gibi çalışır.

**Bilmen gerekenler:**

- Görüntü **Cloudflare** üzerinden aktarılır; TLS orada sonlanır, yani teknik
  olarak görebilirler. USB ve WiFi modlarında böyle bir şey yoktur.
- Tünel, Cloudflare'ın Quick Tunnel hizmetini kullanır; Cloudflare bunu test ve
  geliştirme için tasarlandığını, kesintisizlik garantisi olmadığını belirtir.
  Özelliğin deneysel sayılmasının sebebi budur.
- Yerel ağa göre **daha yüksek gecikme** ve gerçek **mobil veri tüketimi**
  bekle — kalite seçeneklerinin yanında saatlik tahmin yazar.
- Her oturumda yeni bir adres ve yeni bir 128-bit anahtar üretilir. Anahtar
  kabloya hiç çıkmaz, arka arkaya hatalı denemede dinleyici kapanır.
- Uzak mod **varsayılan olarak kapalıdır** ve sen kapatınca durur.

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

## Gizlilik

USB ve yerel WiFi her şeyi kendi cihazlarında tutar — görüntü ne bilgisayarından
ne de ağından çıkar.

Uzak mod bunun istisnasıdır: görüntüyü tasarım gereği Cloudflare ağı üzerinden
geçirir, çünkü port açmadan bağlantıyı mümkün kılan şey budur. Sen açmadıkça
çalışmaz.

## Lisans

MIT — bkz. [LICENSE](../../LICENSE).
