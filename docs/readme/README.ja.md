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
- **リモートモード（実験的）** — モバイル回線を含め、どこからでもスマホを使用。
  ポート開放もアカウントも不要
- **10 言語**、6 テーマ、ダーク UI、トレイ対応
- USB と WiFi は**すべて端末内**で完結

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
4. ビデオアプリでカメラ **「FlexCam」**（OBS を使う場合は
   **「OBS Virtual Camera」**）を選択。

> USB は**USB デバッグ**の有効化が必要（開発者向けオプション）。WiFi はケーブル
> 不要。

## リモート接続（実験的）

リモートモードでは、スマホが**どのネットワークからでも** PC に接続できます。別の
WiFi、友人宅、モバイル回線でも同じです。設定は不要で、ポート開放もルーター設定も
アカウントもいりません。

1. PC で**リモート接続**を開き、画質を選びます。
2. FlexCam が一時的なトンネルを開き、**QR コード**を表示します。
3. スマホで**リモート接続 → QR コードを読み取る**をタップします。

**知っておくこと：**

- 映像は **Cloudflare** を経由し、そこで TLS が終端されるため技術的には内容を見る
  ことができます。USB と WiFi ではこれは起きません。
- Cloudflare は Quick Tunnel をテストと開発向けとし、稼働保証はないと明記していま
  す。そのため本機能は実験的な位置づけです。
- ローカル接続より**遅延が大きく**、実際に**通信量**を消費します。画質ごとに 1
  時間あたりの目安を表示します。
- セッションごとに新しいアドレスと 128 ビットの秘密鍵を生成します。鍵が送信される
  ことはなく、誤りが続くと待ち受けを停止します。
- リモートモードは**既定でオフ**です。

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

## プライバシー

USB とローカル WiFi では、すべてが自分の端末内に留まります。

リモートモードだけは例外で、設計上 Cloudflare のネットワークを経由します。ポートを
開けずに接続できるのはそのためです。自分で有効にしたときだけ動作します。

## ライセンス

MIT — [LICENSE](../../LICENSE) を参照。
