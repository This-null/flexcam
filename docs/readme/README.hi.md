<div align="center">

<img src="../../release/flexcam-logo.png" width="96" alt="FlexCam" />

# FlexCam

**अपने फ़ोन को USB या WiFi से PC वेबकैम बनाएँ।**

[🇬🇧 English](../../README.md) · 🇮🇳 हिन्दी

[Discord](https://discord.gg/EaNcFyCEqP) ·
[Instagram](https://instagram.com/null.rb) ·
[☕ Buy me a coffee](https://buymeacoffee.com/skydev)

</div>

---

## यह क्या है

FlexCam आपके Android फ़ोन के कैमरे को PC पर स्ट्रीम करता है और उसे एक
**वर्चुअल वेबकैम** के रूप में दिखाता है, ताकि कोई भी ऐप (Zoom, Teams, Discord,
ब्राउज़र, OBS) उसे कैमरे के रूप में चुन सके। यह **USB** (ADB) और **WiFi** पर काम
करता है, और एक के टूटने पर अपने आप दूसरे पर चला जाता है।

- हाइब्रिड **USB + WiFi**, स्वतः फ़ेलओवर
- फ़ोन तैयार होने पर **स्वतः कनेक्ट**
- फ़ोन और PC दोनों पर **लाइव प्रीव्यू**
- **आगे / पीछे** कैमरा, **स्वतः पोर्ट्रेट/लैंडस्केप**
- **स्क्रीन बंद** होने पर भी स्ट्रीमिंग जारी
- **WiFi एक्सेस कोड** — आपके नेटवर्क के अजनबी स्ट्रीम नहीं देख सकते
- **10 भाषाएँ**, डार्क UI, ट्रे समर्थन
- पूरी तरह आपके डिवाइस पर चलता है — **कोई डेटा बाहर नहीं जाता**

## वर्चुअल कैमरा ड्राइवर

FlexCam को PC पर एक वर्चुअल कैमरा चाहिए। आपके पास दो विकल्प हैं:

- **साथ में शामिल ड्राइवर (OBS की ज़रूरत नहीं):** पहली बार चलाने पर अगर कोई
  वर्चुअल कैमरा न मिले, तो ऐप में **"वर्चुअल कैमरा इंस्टॉल करें"** पर क्लिक करें।
  यह एक छोटा ओपन-सोर्स ड्राइवर
  ([Unity Capture](https://github.com/schellingb/UnityCapture), MIT) एक बार,
  एक व्यवस्थापक अनुमति के साथ, रजिस्टर करता है।
- **OBS Studio:** अगर आपके पास पहले से [OBS](https://obsproject.com/download) है,
  तो FlexCam उसका वर्चुअल कैमरा अपने आप उपयोग करता है।

## जल्दी शुरू करें

1. **फ़ोन:** `FlexCam.apk` इंस्टॉल करें और ऐप खोलें।
2. **PC:** **FlexCam-Windows.zip** को अनज़िप करें और `FlexCam.exe` चलाएँ।
   - पहली बार: पूछे जाने पर **"वर्चुअल कैमरा इंस्टॉल करें"** पर क्लिक करें (एक बार)।
3. USB से **स्वतः कनेक्ट** होता है। WiFi के लिए फ़ोन का IP और ऐप में दिखाया गया
   **एक्सेस कोड** लिखें।
4. अपने वीडियो ऐप में कैमरा **"OBS Virtual Camera"** (शामिल ड्राइवर के साथ
   **"Unity Video Capture"**) चुनें।

> USB के लिए **USB डिबगिंग** चालू होना चाहिए (डेवलपर विकल्प)। WiFi को केबल की
> ज़रूरत नहीं।

## सोर्स से बनाएँ

**Android (APK):**
```
cd android
gradlew assembleDebug
```
> JDK 17 आवश्यक है।

**PC (डेस्कटॉप ऐप):**
```
cd pc
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python webgui.py
```

PyInstaller (onedir) से स्टैंडअलोन `.exe` — अंग्रेज़ी README में कमांड देखें।

## तकनीक

- **Android:** Kotlin, CameraX, पोर्ट `8474` पर MJPEG सर्वर।
- **PC:** Python, pywebview UI, `pyvirtualcam` → OBS या Unity Capture।
- **ट्रांसपोर्ट:** `adb forward` (USB) या फ़ोन के IP (WiFi) पर रॉ TCP।

## लाइसेंस

MIT — देखें [LICENSE](../../LICENSE)।
