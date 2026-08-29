# Third-party notices

FlexCam's own source code is licensed under the MIT License (see [LICENSE](LICENSE)).

The prebuilt Windows application distributed on the releases page bundles the
third-party components listed below. Because it includes **pyvirtualcam**,
which is licensed under the GNU General Public License v2.0, the bundled
Windows build as a whole is distributed under the terms of the **GPL-2.0**.
The complete corresponding source code is available at
https://github.com/This-null/flexcam — the MIT licensing of FlexCam's own
source is unaffected.

## Bundled components

| Component | Version | License |
| --- | --- | --- |
| [pyvirtualcam](https://github.com/letmaik/pyvirtualcam) | 0.15.0 | GPL-2.0 |
| [pystray](https://github.com/moses-palmer/pystray) | 0.19.5 | LGPL-3.0 |
| [pywebview](https://github.com/r0x0r/pywebview) | 6.2.1 | BSD-3-Clause |
| [Pillow](https://github.com/python-pillow/Pillow) | 12.3.0 | MIT-CMU |
| [NumPy](https://github.com/numpy/numpy) | 2.5.2 | BSD-3-Clause |
| [pypresence](https://github.com/qwertyquerty/pypresence) | 4.6.2 | MIT |
| [Unity Capture](https://github.com/schellingb/UnityCapture) filter | — | MIT |
| Android Debug Bridge (`adb`) | — | Android SDK terms |

Unity Capture is Copyright (c) 2018 Bernhard Schelling, based on UnityCam,
Copyright (c) 2016 MHD Yamen Saraiji. Its full license text ships with the
application in `virtualcam/LICENSE-UnityCapture.txt`.

`adb.exe` and its DLLs are part of the Android SDK Platform-Tools, distributed
by Google under the Android Software Development Kit License Agreement.
