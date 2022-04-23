---
title: PlatformIO
parent: Writing C++ Applications
nav_order: 2
---
## PlatformIO

In the first time, PlatformIO is a bit more complicated than Arduino IDE, but it has many advantages.
For example, you could choose your own IDE. Compile times are much faster. 

Since you could choose your own IDE, you need to decide which one you want to use. 
If you don't know which IDE to use, try using Visual Studio Code, because it's free. 
You could use any other PlatformIO compatible IDE as well.

### Visual Studio Code

1. Download and install the IDE [Visual Studio Code](https://code.visualstudio.com/)

2. Download and install the latest version of [PlatformIO](https://platformio.org/install/ide?install=vscode).

3. If you are a VS Code beginner, read the [quick start guide](https://docs.platformio.org/page/ide/vscode.html#quick-start)

4. Create a new PlatformIO project (use the home button in VS Codes purple status bar)
- Board: `Espressif ESP 32 Dev Module`
- Framework: `Arduino Framework`

5. Wait for VSCode setting up your project.

6. Change content of `platformio.ini` to
```ini
[env:esp32dev]
platform = https://github.com/platformio/platform-espressif32.git#eff0222cd1ce270a9c5f6d183e6e240f5e5cd458
board = esp32dev
framework = arduino
lib_deps = bloeckchengrafik/ftSwarm
```


7. Start writing your code. Use the following elements of the blue statusbar:
- ![Home](/assets/img/vs_home.png) opens platformIO home. 
- ![build](/assets/img/vs_build.png) builds your software.
- ![upload](/assets/img/vs_upload.png) uploads/flashes your software.
- ![clean](/assets/img/vs_clean.png) cleans up your cached files.
- ![serial](/assets/img/vs_serial.png) opens the serial monitor.
- ![terminal](/assets/img/vs_terminal.png) opens a terminal.
- ![switch](/assets/img/vs_switch.png) switches between your projects.


## CLion

1. Download and install the IDE [CLion](https://www.jetbrains.com/clion/)

2. Download and install the latest version of [PlatformIO](https://docs.platformio.org/en/latest//integration/ide/clion.html). 

3. Create a new PlatformIO project in your IDE using the Board `Espressif ESP 32 Dev Module/esp32dev`
- Add the line `lib_deps = bloeckchengrafik/ftSwarm` to your `platformio.ini`
- Change the `platform = espressif32` to `platform = https://github.com/platformio/platform-espressif32.git#eff0222cd1ce270a9c5f6d183e6e240f5e5cd458`

4. Run `pio run` to download and build all libraries.

<br>
[Run your first application: motor&switch](../3_MotorSwitch){: .btn .float-right }
<br>