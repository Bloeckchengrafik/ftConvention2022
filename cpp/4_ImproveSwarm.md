---
title: Improve Your Swarm
parent: Writing C++ Applications
nav_order: 4
---

## Improve Your Swarm

Up to now the IO's were identified by the serial number and the name of the port. This is nice in a small setup, but it could be confusing in a bigger setup.
This example uses alias names. So you don’t have to code which actuator or sensor uses which physical IO-pin in your code.

Use the setup of [Using The Swarm](3_UseSwarm).

First, you need to set the alias names for switch and motor. Therefore you need to call the firmware's setup routine:

```cpp
#include <ftSwarm.h>

void setup() {
  ftSwarm.begin();
  ftSwarm.setup();
}

void loop() {
}
```

Connect via usb and terminal program. Set the alias `switch` for port A01 as described in [Configure Your Device](../setup/30_configure_your_device).
Since the second device is running the standard firmware, you don't need to upload this snippet. Just connect via USB and set the alias `motor`for port M01.

Now we need to modify both lines to instantiate switch and motor:

```
#include "ftSwarm.h"

// serial number of the second controller - change it to your 2nd device serial number
#define remote = 2

FtSwarmSwitch *switch;
FtSwarmMotor  *motor;

void setup( ) {

  // start the swarm
  FtSwarmSerialNumber local = ftSwarm.begin( );
	
  // get switch and motor instances
  switch = new FtSwarmSwitch( "switch" );
  motor  = new FtSwarmMotor( "motor" );

}

void loop( ) {

  // check if switch is pressed or released
  if ( switch->isPressed() )
    motor->setSpeed(255);
  else
    motor->setSpeed(0);
	
  // wait some time
  delay(100);

}
```

Let's look at the monitor page of your swarm. The IO's show their alias names as well.

Finally, modify your hardware setup. Move your motor to port M02 of your first device. Set the alias "motor" at your first device. Start the application again. It's running without any changes!.

*But keep in mind, an alias name needs to be unique in your swarm! In this example it doesn't matter to define "motor" twice. 
The firmware alsways checks the local device alias names first. But using multiple remote devices, the result depends on the boot sequence of the remote devices.*
 
