<div align="center">

<img src="../../release/flexcam-logo.png" width="96" alt="FlexCam" />

# FlexCam

**通过 USB 或 WiFi，把手机变成电脑网络摄像头。**

[🇬🇧 English](../../README.md) · 🇨🇳 中文

[Discord](https://discord.gg/EaNcFyCEqP) ·
[Instagram](https://instagram.com/null.rb) ·
[☕ Buy me a coffee](https://buymeacoffee.com/skydev)

</div>

---

## 这是什么

FlexCam 把安卓手机的摄像头串流到电脑，并显示为一个**虚拟网络摄像头**，
这样任何应用（Zoom、Teams、Discord、浏览器、OBS）都能把它当作摄像头。
它通过 **USB**（ADB）和 **WiFi** 工作，其中一个断开时会自动切换。

- **USB + WiFi** 混合，自动切换
- 手机就绪时**自动连接**
- 手机和电脑上都有**实时预览**
- **前置 / 后置**摄像头，**自动竖屏/横屏**
- **息屏**时继续串流
- **WiFi 访问码** — 网络中的陌生人无法查看你的画面
- **10 种语言**，深色界面，托盘支持
- 完全在你的设备上运行 — **没有任何数据离开你的电脑**

## 虚拟摄像头驱动

FlexCam 需要电脑上的虚拟摄像头。你有两个选择：

- **内置驱动（无需 OBS）：** 首次运行时如果未找到虚拟摄像头，点击应用中的
  **“安装虚拟摄像头”**。它会一次性注册一个小型开源驱动
  （[Unity Capture](https://github.com/schellingb/UnityCapture)，MIT），
  需要一次管理员确认。
- **OBS Studio：** 如果你已安装 [OBS](https://obsproject.com/download)，
  FlexCam 会自动使用它的虚拟摄像头。

## 快速开始

1. **手机：** 安装 `FlexCam.apk` 并打开应用。
2. **电脑：** 解压 **FlexCam-Windows.zip** 并运行 `FlexCam.exe`。
   - 首次运行：如有提示，点击**“安装虚拟摄像头”**（仅一次）。
3. 通过 USB **自动连接**。使用 WiFi 时，输入手机 IP 和应用中显示的**访问码**。
4. 在你的视频应用中，选择摄像头 **“OBS Virtual Camera”**
   （若使用内置驱动则为 **“Unity Video Capture”**）。

> USB 需要开启**USB 调试**（开发者选项）。WiFi 不需要线缆。

## 从源码构建

**Android (APK):**
```
cd android
gradlew assembleDebug
```
> 需要 JDK 17。

**PC（桌面应用）：**
```
cd pc
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python webgui.py
```

用 PyInstaller（onedir）打包独立 `.exe` — 见英文 README 中的命令。

## 技术

- **Android：** Kotlin、CameraX，端口 `8474` 上的 MJPEG 服务器。
- **PC：** Python、pywebview 界面、`pyvirtualcam` → OBS 或 Unity Capture。
- **传输：** 通过 `adb forward`（USB）或手机 IP（WiFi）的原始 TCP。

## 许可证

MIT — 见 [LICENSE](../../LICENSE)。
