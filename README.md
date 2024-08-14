A shock sensor for pre-season events logging to SD card.
credit to the zebracorns:
https://github.com/FRC900/2023RobotCode/blob/main/zebROS_ws/src/adafruit_adxl37x/src/Ada_the_fruit_on_the_acceleratormator.py

Porting to pico-w for network time sync.

There are 2 use cases for this:
1. Running in constant output mode to the serial feed.  Can be hooked to a PC running Thonny to graph the output live
2. Logging to the SD card. A capture threshold is set, A stop capture threshold is set, and a Max Time/datapoints is set. Once the shock threshold is reached, it logs to memory until it reaches the Min threshold, or the Max Data points.  Then it logs the data to SD card, then  goes back to watching for a shock event.

Use Case 1 is for testing and for testing bumper designs
Use Case 2 is for capturing data over a competition.

At power-on it should try to join a defined Wi-Fi network.
Fetch NTP Time
then go into either mode 1 or mode 2 depending on setting.


