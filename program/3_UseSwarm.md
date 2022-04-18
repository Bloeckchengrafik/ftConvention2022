---
title: Using The Swarm
parent: Writing Applications
nav_order: 2
---

## Using The Swarm

[The First Application](../2_1stApp) was nice to show how a ftSwarm application is coded. But it was just a simple "one-controller-application".
Now it's time to use the swarm. The application's idea is the same - control a motor by a switch. But in this application, switch and motor
are connected to different controllers:

- Use the setup of [The First Application](../2_1stApp).
- Add a second ftSwarm or ftSwarmControl device.
- Connect a 9V power supply to your second device.
- Move the motor to M2 of the new device.

To run this program, both ftSwarm devices need to be connected in a swarm.

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
  switch = new FtSwarmSwitch( local, FTSWARM_A01 );
  motor  = new FtSwarmMotor( remote, FTSWARM_M02 );

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

Basically, the application is the same as [The First Application](../2_1stApp). There are only two changes:

- `#define remote=2` sets the serial number of your 2nd device. Please change the serial number to your 2nd device serial number.
- `FtSwarmMotor( remote, FTSWARM_M02 );` now uses the remote device serial number instead of the local serial number.

On the monitor page of your first device, you will now see both controllers.

Start the serial monitor and unplug the 9V power suplly from the second device. Restart the first one. 
With `FtSwarmMotor( remote, FTSWARM_M02 );` you will get the debug output `Waiting on device`. The firmware waits on the motor IO joining the swarm.
Add the 9V power supply again. Once the second device is started, your application will continue.

This feature helps you starting a swarm based roboter. You don't need to think about the timing or sequence of starting your devices.