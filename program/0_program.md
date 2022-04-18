---
title: Writing Applications
nav_order: 3
has_children: true
---

## Writing Applications

In classic robotics you work with one central contol unit, which drives all actuators and sensors.
You just need to write one application, which controls all IO's. That's easy, in an Arduino environment you just have to write two procedures: 
- `setup` is just called one time and initializes all of your hardware.
- Your actual functionality is coded in the procedure `loop`, which runs in a loop.
Complexity starts, if you start using interrupts and threads.

By using multiple controllers in a swarm, you get a distributed system. Now every controller needs it's own application. So you get a bunch of threads, 
who need to be coordinated via network. To resolve this complexity, the ftSwarm firmware uses "The Kelda Principle".
