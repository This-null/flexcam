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

> [!CAUTION]
> **FlexCam'in çalışması için [OBS Studio](https://obsproject.com/download) kurulu olmalıdır.**
> Telefonu webcam olarak göstermek için OBS Virtual Camera sürücüsünü kullanır.
> OBS'i bir kez kur — açık tutmana gerek yok.

---

## Nedir

FlexCam, Android telefonunun kamerasını PC'ne aktarır ve **"OBS Virtual Camera"**
olarak gösterir; böylece herhangi bir uygulama (Zoom, Teams, Discord, tarayıcı,
OBS) onu webcam olarak seçebilir. **USB** (ADB) ve **WiFi** üzerinden çalışır,
biri koparsa otomatik olarak diğerine geçer.

- Hibrit **USB + WiFi**, otomatik yük devretme
- Telefon hazır olunca **otomatik bağlanır** — elle işlem yok
- **Ön / arka** kamera geçişi
- **Otomatik dik/yatay** (telefonun yönünü izler)
- **Ekran kapalıyken** de yayın sürer
- **10 dil**, koyu arayüz, tepsi desteği
- Tamamen cihazında çalışır — **hiçbir veri dışarı gönderilmez**

## Hızlı başlangıç

1. **OBS Studio** kur (bir kez).
2. Telefonda: `release/FlexCam.apk` kur ve uygulamayı aç.
3. PC'de: **FlexCam**'i çalıştır, otomatik bağlanır.
4. Video uygulamanda kamera olarak **"OBS Virtual Camera"** seç.

USB için **USB hata ayıklama** açık olmalı (Geliştirici Seçenekleri). WiFi kablo
istemez — uygulamanın gösterdiği IP'yi yaz.

## Lisans

MIT — bkz. [LICENSE](../../LICENSE).
