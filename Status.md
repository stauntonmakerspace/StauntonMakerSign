# Makersign Status
## Thursday, November 4 2021

Each letter in the sign is controlled by an Arduino
Each led cmd of the consist of six bytes 
* Start Byte, device_num, Red, Green, Blue


## Issues to Solve:
* And the current sign consists of two board types a Pro Mini Board and a Nano Board
  * Both present issues of their own
  * The nano boards were manufactured in house and are falling apart. The solder joints are delicate so I 
  * The pro mini version requires that clip and cables be use for data communication this was an attempt to reduce issues with cable walking but the short bins that the cables experience with and assign leads them to Frank and due to their size they are tedious to remake 
* There are still several optimizations that can be implemented in order to achieve higher frame rates
* There is a minimum of a 50 µs delay that needs to happen between the sending of each command otherwise data communication becomes unreliable
  * Redesigned would increase the size of the serial buffer so that communication can happen faster 
* The configurator