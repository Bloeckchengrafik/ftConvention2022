#include <Arduino.h>
#include "ftSwarm.h"

FtSwarmLED *led;

void setup() {

   Serial.begin(115200);

   // start the swarm
   ftSwarm.verbose(true);
   FtSwarmSerialNumber_t local = ftSwarm.begin( false );
   
   led = new FtSwarmLED(local, 17);
   
   led->setColor(0xffffff);
   led->setBrightness(100);

}

void loop() {
  delay(250);
}