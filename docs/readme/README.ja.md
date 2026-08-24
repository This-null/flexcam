<div align="center">

<img src="../../release/flexcam-logo.png" width="96" alt="FlexCam" />

# FlexCam

**スマホを USB または WiFi で PC のウェブカメラに。**

[🇬🇧 English](../../README.md) · 🇯🇵 日本語

[Discord](https://discord.gg/EaNcFyCEqP) ·
[Instagram](https://instagram.com/null.rb) ·
[☕ Buy me a coffee](https://buymeacoffee.com/skydev)

</div>

---

## これは何

FlexCam は Android スマホのカメラを PC にストリーミングし、**仮想ウェブカメラ**
として見せます。これにより、どのアプリ（Zoom、Teams、Discord、ブラウザ、OBS）
でもカメラとして選べます。**USB**（ADB）と **WiFi** で動作し、片方が切れると
自動で切り替わります。

- **USB + WiFi** ハイブリッド、自動フェイルオーバー
- スマホの準備ができると**自動接続**
- スマホと PC の両方で**ライブプレビュー**
- **前面 / 背面**カメラ、**自動で縦/横**
- **画面オフ**でも配信継続
- **WiFi アクセスコード** — ネットワーク上の他人は映像を見られません
- **10 言語**、ダーク UI、トレイ対応
- すべて端末内で動作 — **データがパソコンから出ることはありません**

## 仮想カメラドライバー

FlexCam は PC 上の仮想カメラが必要です。2 つの方法があります：

- **同梱ドライバー（OBS 不要）：** 初回起動時に仮想カメラが見つからない場合、
  アプリの **「仮想カメラをインストール」** をクリック。小さなオープンソース
  ドライバー（[Unity Capture](https://github.com/schellingb/UnityCapture)、MIT）
  を一度だけ、管理者確認付きで登録します。
- **OBS Studio：** すでに [OBS](https://obsproject.com/download) がある場合、
  FlexCam はその仮想カメラを自動的に使います。

## クイックスタート

1. **スマホ：** `FlexCam.apk` をインストールしてアプリを開く。
2. **PC：** **FlexCam-Windows.zip** を解凍し `FlexCam.exe` を起動。
   - 初回：求められたら **「仮想カメラをインストール」**（一度だけ）。
3. USB で**自動接続**します。WiFi の場合はスマホの IP とアプリに表示される
   **アクセスコード**を入力。
4. ビデオアプリでカメラ **「OBS Virtual Camera」**（同梱ドライバー使用時は
   **「Unity Video Capture」**）を選択。

> USB は**USB デバッグ**の有効化が必要（開発者向けオプション）。WiFi はケーブル
> 不要。

## ソースからビルド

**Android (APK):**
```
cd android
gradlew assembleDebug
```
> JDK 17 が必要。

**PC（デスクトップアプリ）：**
```
cd pc
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python webgui.py
```

PyInstaller（onedir）でスタンドアロン `.exe` — 英語 README のコマンドを参照。

## 技術

- **Android：** Kotlin、CameraX、ポート `8474` の MJPEG サーバー。
- **PC：** Python、pywebview UI、`pyvirtualcam` → OBS または Unity Capture。
- **転送：** `adb forward`（USB）またはスマホの IP（WiFi）経由の生 TCP。

## ライセンス

MIT — [LICENSE](../../LICENSE) を参照。
