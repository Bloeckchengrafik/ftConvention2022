---
title: PlatformIO
parent: Writing C++ Applications
nav_order: 2
---
## PlatformIO

PlatformIO is a bit more complicated to set up than the Arduino IDE, but it has many advantages. For example, it allows to use a different IDE and compile faster. 

To install and configure PlatformIO for the development with the ftSwarm, please use the following steps: 

- Download and install the latest version of PlatformIO for your IDE ([Visual Studio Code](https://platformio.org/install/ide?install=vscode)/[Jetbrains CLion](https://docs.platformio.org/en/latest//integration/ide/clion.html)). If you don't know which IDE to use, try using [Visual Studio Code](https://code.visualstudio.com/)
- Start your IDE and create a new PlatformIO project with the Board `Espressif ESP 32 Dev Module`/`esp32dev`
- Add the line `lib_deps = bloeckchengrafik/ftSwarm` to your `platformio.ini`
- Change the line `platform = espressif32` to `platform = https://github.com/platformio/platform-espressif32.git#eff0222cd1ce270a9c5f6d183e6e240f5e5cd458`
- Run `pio run` to download and build all libraries