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
- **远程模式（实验性）** — 随时随地使用手机，包括移动数据；无需端口转发，无需账号
- **10 种语言**、6 种主题、深色界面、托盘支持
- USB 和 WiFi **完全在你的设备上**运行

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
4. 在你的视频应用中，选择摄像头 **“FlexCam”**
   （若使用 OBS 则为 **“OBS Virtual Camera”**）。

> USB 需要开启**USB 调试**（开发者选项）。WiFi 不需要线缆。

## 远程连接（实验性）

远程模式让手机可以从**任何网络**连接到你的电脑 —— 另一个 WiFi、朋友家，或者移动
数据。无需任何配置：不用端口转发，不用改路由器，也不用账号。

1. 在电脑上打开**远程连接**并选择画质。
2. FlexCam 会开启一条临时隧道并显示**二维码**。
3. 在手机上点击**远程连接 → 扫描二维码**。

**你需要知道：**

- 视频经由 **Cloudflare** 转发，TLS 在那里终止，因此技术上他们可以看到内容。
  USB 与 WiFi 模式不会这样。
- Cloudflare 说明 Quick Tunnel 仅供测试与开发使用，不保证可用性，所以此功能标记
  为实验性。
- 延迟会**高于局域网**，并且会消耗**真实的移动数据**；每个画质旁都有每小时的估算。
- 每次会话都会生成新地址和新的 128 位密钥。密钥从不在网络上传输，多次错误尝试后
  会关闭监听。
- 远程模式**默认关闭**。

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

## 隐私

USB 和局域网 WiFi 会把一切保留在你自己的设备上。

远程模式是例外：它按设计通过 Cloudflare 的网络转发视频，因为这正是无需开放端口即可
建立连接的原因。只有你开启时才会运行。

## 许可证

MIT — 见 [LICENSE](../../LICENSE)。
