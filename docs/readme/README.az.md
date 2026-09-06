<div align="center">

<img src="../../release/flexcam-logo.png" width="96" alt="FlexCam" />

# FlexCam

**Telefonunu USB və ya WiFi ilə PC veb-kamerasına çevir.**

[🇬🇧 English](../../README.md) · 🇦🇿 Azərbaycan

[Discord](https://discord.gg/EaNcFyCEqP) ·
[Instagram](https://instagram.com/null.rb) ·
[☕ Buy me a coffee](https://buymeacoffee.com/skydev)

</div>

---

## Nədir

FlexCam Android telefonunun kamerasını PC-yə ötürür və onu **virtual veb-kamera**
kimi göstərir; beləliklə istənilən tətbiq (Zoom, Teams, Discord, brauzer, OBS)
onu kamera kimi seçə bilər. **USB** (ADB) və **WiFi** üzərindən işləyir və biri
kəsilsə avtomatik digərinə keçir.

- Hibrid **USB + WiFi**, avtomatik keçid
- Telefon hazır olanda **avtomatik qoşulur**
- Telefonda və PC-də **canlı önizləmə**
- **Ön / arxa** kamera, **avtomatik dik/üfüqi**
- **Ekran bağlı** ikən yayım davam edir
- **WiFi giriş kodu** — şəbəkədəki yad adamlar yayımı görə bilməz
- **Uzaq rejim (sınaq)** — telefonunu hər yerdən, hətta mobil data ilə
  istifadə et; port yönləndirmə və hesab tələb olunmur
- **10 dil**, 6 tema, qaranlıq interfeys, trey dəstəyi
- USB və WiFi **tamamilə cihazında** işləyir

## Virtual kamera sürücüsü

FlexCam PC-də virtual kameraya ehtiyac duyur. İki seçimin var:

- **Daxili sürücü (OBS lazım deyil):** İlk açılışda virtual kamera tapılmasa,
  tətbiqdə **"Virtual kamera quraşdır"** düyməsinə bas. Kiçik, açıq mənbəli bir
  sürücünü ([Unity Capture](https://github.com/schellingb/UnityCapture), MIT)
  bir dəfəlik admin icazəsi ilə qeydiyyatdan keçirir.
- **OBS Studio:** Artıq [OBS](https://obsproject.com/download) quraşdırılıbsa,
  FlexCam onun virtual kamerasını avtomatik istifadə edir.

## Sürətli başlanğıc

1. **Telefon:** `FlexCam.apk`-ı quraşdır və tətbiqi aç.
2. **PC:** **FlexCam-Windows.zip**-i aç və `FlexCam.exe`-ni işə sal.
   - İlk açılış: soruşulsa **"Virtual kamera quraşdır"**a bas (bir dəfəlik).
3. USB üzərindən **avtomatik qoşulur**. WiFi üçün telefonun IP-sini və tətbiqdə
   göstərilən **giriş kodunu** yaz.
4. Video tətbiqində kamera olaraq **"FlexCam"** seç (OBS istifadə edirsənsə
   **"OBS Virtual Camera"**).

> USB üçün **USB debugging** aktiv olmalıdır (Developer Options). WiFi kabel
> tələb etmir.

## Uzaqdan bağlantı (sınaq)

Uzaq rejim telefonun **istənilən şəbəkədən** kompüterinə çatmasına imkan verir —
başqa WiFi, dostunun evi və ya mobil data. Heç nə qurmaq lazım deyil: port
yönləndirmə yox, modem ayarı yox, hesab yox.

1. Kompüterdə **Uzaqdan bağlantı**-nı aç və keyfiyyət seç.
2. FlexCam müvəqqəti tunel açır və bir **QR kod** göstərir.
3. Telefonda **Uzaqdan qoşul → QR kodu oxut** düyməsinə toxun.

**Bilməli olduqların:**

- Video **Cloudflare** üzərindən ötürülür; TLS orada bitir, yəni texniki olaraq
  görə bilərlər. USB və WiFi rejimlərində bu baş vermir.
- Cloudflare Quick Tunnel-ları sınaq və inkişaf üçün nəzərdə tutulmuş kimi
  təsvir edir, işləmə zəmanəti yoxdur — buna görə funksiya sınaq sayılır.
- Yerli şəbəkəyə nisbətən **daha yüksək gecikmə** və real **mobil data
  sərfiyyatı** gözlə; keyfiyyət seçimlərinin yanında saatlıq təxmin yazılıb.
- Hər sessiyada yeni ünvan və yeni 128-bit açar yaradılır. Açar heç vaxt
  ötürülmür, ardıcıl səhv cəhdlərdən sonra dinləyici bağlanır.
- Uzaq rejim **standart olaraq bağlıdır**.

## Mənbədən qurmaq

**Android (APK):**
```
cd android
gradlew assembleDebug
```
> JDK 17 tələb olunur.

**PC (masaüstü tətbiqi):**
```
cd pc
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python webgui.py
```

Müstəqil `.exe` PyInstaller (onedir) ilə — ingilis README-dəki əmrə bax.

## Texnologiya

- **Android:** Kotlin, CameraX, `8474` portunda MJPEG server.
- **PC:** Python, pywebview interfeys, `pyvirtualcam` → OBS və ya Unity Capture.
- **Ötürmə:** `adb forward` (USB) və ya telefonun IP-si (WiFi) üzərindən xam TCP.

## Məxfilik

USB və yerli WiFi hər şeyi öz cihazlarında saxlayır.

Uzaq rejim istisnadır: videonu qəsdən Cloudflare şəbəkəsi üzərindən ötürür,
çünki port açmadan bağlantını mümkün edən budur. Yalnız sən açanda işləyir.

## Lisenziya

MIT — bax [LICENSE](../../LICENSE).
