# SPDX-FileCopyrightText: 2024 Team 4160 The RoBucs with code from Team 900 The Zebracorns
#
# SPDX-License-Identifier: BSD 3-Clause License
#
# Notes and salutations
# The default startup is to light all lights (1-5), calculate a "Noise" threshold (2-3 lit), then wait for the first shock event (2,3,4 Lit).
# This allows you to sync up multiple units all to the same "time_sync_event". 
# To sync them up: Put all the units on the same surface, wait till 2,3,4 are lit, then hit the surface with a hammer.
# they should all go red (1) then green (5)

# LED Statuses:
# 1 blinking fast for 10 seconds: Something wrong with SD Card.
# all LED on: stuck in boot.
# 2&3 lit: Calculating Noise threshold
# 2,3,4 Lit: Waiting for First event
# 4 lit: Waiting for shock
# 1 single blink less than 2 seconds : Writing to SD card



import board
import busio
import sdcardio
import storage
import digitalio
import time
import adafruit_adxl37x
from adafruit_adxl34x import DataRate
import math
import gc

##
# Settings
##

# what is the initial clock
print("\nInitial Clock")
power_on_time = time.monotonic()
print(power_on_time)

#settings
samples_per_sec = 32
sample_sec = 1/samples_per_sec
baseline_samples = 64
max_samples = 60
min_threshold = 30

# Functions
def LED_on(LED_num):
    if LED_num == 1:
        LED_1.value = True
    elif LED_num == 2:
        LED_2.value = True
    elif LED_num == 3:
        LED_3.value = True
    elif LED_num == 4:
        LED_4.value = True
    elif LED_num == 5:
        LED_5.value = True
    else:
        print("invalid LED")
def LED_off(LED_num):
    if LED_num == 1:
        LED_1.value = False
    elif LED_num == 2:
        LED_2.value = False
    elif LED_num == 3:
        LED_3.value = False
    elif LED_num == 4:
        LED_4.value = False
    elif LED_num == 5:
        LED_5.value = False
    else:
        print("invalid LED")

# bps * s should be an interger
def LED_blink(LED_num, bps, s):
    for i in range(bps * s):
        LED_on(LED_num)
        time.sleep (0.5/bps)
        LED_off(LED_num)
        time.sleep (0.5/bps)

##
# Setup Devices and LED
##

# setup LED's
LED_1 = digitalio.DigitalInOut(board.GP10)
LED_1.direction = digitalio.Direction.OUTPUT
LED_2 = digitalio.DigitalInOut(board.GP9)
LED_2.direction = digitalio.Direction.OUTPUT
LED_3 = digitalio.DigitalInOut(board.GP8)
LED_3.direction = digitalio.Direction.OUTPUT
LED_4 = digitalio.DigitalInOut(board.GP7)
LED_4.direction = digitalio.Direction.OUTPUT
LED_5 = digitalio.DigitalInOut(board.GP6)
LED_5.direction = digitalio.Direction.OUTPUT
# Test all LED
print("LED ON")
for i in range(1,6):
    LED_on(i)
time.sleep(2)
for i in range(1,6):
    LED_off(i)


# setup SD card
print("Setup SD Card")

spi = busio.SPI(board.GP2, MOSI=board.GP3, MISO=board.GP0)
cs = board.GP1
# Create SD CARD object
try:
    sdcard = sdcardio.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
except:
    print("Maybe no SD Card?")
    LED_blink(1,10,10)

try:
    storage.mount(vfs, "/sd")
    try:
        with open("/sd/test.txt", "w") as f:
            f.write("Powered On at:{}\r\n".format(power_on_time))
            f.close()
        LED_on(2)

    except:
        print("Failed to Mount")
        LED_blink(1,10,10)
except:
    print("Failed to Mount")
    LED_blink(1,10,10)

print("Setup Accelerometer")
# setup the connection to the accelerometer device
i2c = busio.I2C(scl=board.GP21, sda=board.GP20)  # Set and define where SCL and SDA are connected.
global accelerometer
accelerometer = adafruit_adxl37x.ADXL375(i2c)
accelerometer.data_rate  = DataRate.RATE_800_HZ
_REG_DATA_FORMAT: int = 0x31
active_change = accelerometer._read_register_unpacked(_REG_DATA_FORMAT)
accelerometer._write_register_byte(_REG_DATA_FORMAT, active_change | 0b00001011) #0b00001011 comes from the adafruit arduino library linked by ty which supposedly fixes the bits at _reg_data_format for 25+ g
LED_on(3)



# calculate a baseline by sampling then calculating the acceleration vector sqrt of X^2 + y^2 + Z^2.
# multiply by a factor for what constitutes an event we want to log.
# because X, Y, Z are squared acceleration vector is always positive.

print("Calibrating a Baseline")

total_acc_vector = 0
for sample in range(1,baseline_samples):
    x,y,z = accelerometer.acceleration
    total_acc_vector = math.sqrt((x**2)+(y**2)+(z**2)) + total_acc_vector

avg_acc_vector_noise = total_acc_vector/baseline_samples
event_threshold = max( (avg_acc_vector_noise *2), min_threshold)
print("\nEvent Threshold:{}\n".format(event_threshold))
LED_on(4)
print("Waiting for first event")

x,y,z = accelerometer.acceleration
while math.sqrt((x**2)+(y**2)+(z**2)) <= event_threshold:
    time.sleep(sample_sec)
    x,y,z = accelerometer.acceleration
time_sync_event = time.monotonic()
for i in range(1,6):
    LED_off(i)

# Now we wait for an event greater than the event_threshold.
# if the event occurs then we want to capture data
print ("Wait for Event")
LED_on(5)

# Tight loop check if the vector of all x, y , z acceleration's is larger than the threshold
# if it is larger than the threshold log data points to memory
# once we log the data points to memory, stop and write them to SD card.
# also log the start and end time to the SD card. This is close enough to the event time and is the time since
# the first shock event.
# finally clear the memory and "Garbage Collect" to keep memory free

while True:
    x,y,z = accelerometer.acceleration
    if math.sqrt((x**2)+(y**2)+(z**2)) >= event_threshold:
        print("Event Start")
        LED_off(5)
        data_list =[(x,y,z)]
        for sample in range (1, max_samples):
#            print(sample)
            x,y,z = accelerometer.acceleration
            data_list.append((x,y,z))
#            print((x,y,z))
            time.sleep(sample_sec)

        #write out data to SD card.
        with open("/sd/data.txt", "a") as data_file:
            data_file.write("\nTimestamp:{}\n".format(time.monotonic()-time_sync_event))
            for line in data_list:
                data_file.write(f"{line}\n")
            data_file.write("Timestamp:{}\n".format(time.monotonic()-time_sync_event))
            data_file.close()
        del data_list
        print(gc.mem_free())
        gc.collect()
        print(gc.mem_free())
        print("Event End")
        LED_blink(1,2,0.5)
        LED_on(5)
