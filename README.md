A shock sensor for pre-season events logging to SD card.
credit to the zebracorns:
https://github.com/FRC900/2023RobotCode/blob/main/zebROS_ws/src/adafruit_adxl37x/src/Ada_the_fruit_on_the_acceleratormator.py

Porting to pico 2040
See circut diagram and case

The default startup is to light all lights (1-5), calculate a "Noise" threshold (2-3 lit), then wait for the first shock event (2,3,4 Lit).
This allows you to sync up multiple units all to the same "time_sync_event".
To sync them up: Put all the units on the same surface, wait till 2,3,4 are lit, then hit the surface with a hammer.
they should all go red (1) then green (5)

LED Statuses:
1 blinking fast for 10 seconds: Something wrong with SD Card.
all LED on: stuck in boot.
2&3 lit: Calculating Noise threshold
2,3,4 Lit: Waiting for First event
4 lit: Waiting for shock
1 single blink less than 2 seconds : Writing to SD card

Running on Adafruit CircuitPython 9.1.3 
Install from: https://circuitpython.org/board/raspberry_pi_pico/
Install adafruit_adxl34x.mpy and adafruit_adxl37x.mpy from the adafruit-circutpython-bundle-9.x into the lib folder of the Pico over USB.
Copy code.py over to the Pico USB drive.

Wire up according to the Impact Sensor.fzz (.png also provided).

Parts List:
SD Card: https://amzn.to/4gctrdu
SD Card Reader: https://amzn.to/3XgmkZ3
LED: https://amzn.to/3My8YCd
~200 Ohm Resistors: https://amzn.to/3AOs7gT
Pico 2040: https://www.adafruit.com/product/4864
ADXL375 Sensor: https://www.adafruit.com/product/5374

Assume that you also have wire, solder, etc..

3D printable case file supplied as well here as a .3mf file and fusion 360 source.
You'll need M2 and M3 screws for the case.


