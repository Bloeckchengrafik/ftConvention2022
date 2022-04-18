---
title: The Kelda Principle
parent: Writing Applications
nav_order: 1
---

## The Kelda Principle

The "The Wee Free Men" in Terry Pratchett's novel with the same name are a chaotic bunch, as each one acts for himself.  The overview in this people has the 
only female being of the clan, the Kelda. She provides the basis of cooperation: what the Kelda says is law and is obeyed.

As in the novel, it is very demanding toget all the small, free controllers under one hat.

For this, the ftSwarm has a simple solution with the Kelda approach: Since all controllers have a powerful ESP32-Wrover processor, one controller in the model 
becomes a Kelda. It takes over the control task and sends control commands to the other controllers via wifi or queries the status of sensors.

So you just write one program with the two procedures `setup`and `loop`. All other controllers just run the standard "firmware". 
By using the ftSwarm-Library, your "Kelda" program could access all of the distributed actuators and sensors easyly.

