---
nav_order: 2
---
## 2. Setting your Arduino IDE

The easiest way to write some code for your ftSwarm is using the arduino IDE. Please use at least version 1.8.19. 2.x beta versions are compatible as well. 

To install and configure your arduino IDE, please use the following steps: 

- Download and install the latest version of arduino ide from [arduino.cc](https://www.arduino.cc/en/software).
- Start arduino ide, select `File/Preferences`. Add "https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json" to "Additional Board Manager URLs.
- Open `Tools/Boards Manager` and install `esp32 by espressif systems`. You need at least **version 2.02**. Check `Additional Boards Manager URLs` if only 1.x versions are listed.
- Install the following libraries in `Tools\Manage Libraries`:
    - Adafruit GFX Library
    - FastLED by Daniel Garcia
- Finally, you need to install the ftSwarm library. Download latest ftswarm.zip 
