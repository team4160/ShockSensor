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
# what is the initial clock
print("\nInitial Clock")
power_on_time = time.monotonic()
print(power_on_time)

#settings
samples_per_sec = 32
sample_sec = 1/samples_per_sec
baseline_samples = 32
max_samples = 60

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

try:
    storage.mount(vfs, "/sd")
    try:
        with open("/sd/test.txt", "w") as f:
            f.write("Hello world!\r\n")
            f.close()
    except:
        print("Failed to Mount")
except:
    print("Failed to Mount")

print("Setup Accelerometer")
# setup the connection to the accelerometer device
i2c = busio.I2C(scl=board.GP21, sda=board.GP20)  # Set and define where SCL and SDA are connected.
global accelerometer
accelerometer = adafruit_adxl37x.ADXL375(i2c)
accelerometer.data_rate  = DataRate.RATE_800_HZ
_REG_DATA_FORMAT: int = 0x31
active_change = accelerometer._read_register_unpacked(_REG_DATA_FORMAT)
accelerometer._write_register_byte(_REG_DATA_FORMAT, active_change | 0b00001011) #0b00001011 comes from the adafruit arduino library linked by ty which supposedly fixes the bits at _reg_data_format for 25+ g



# calculate a baseline by sampling then calculating the acceleration vector sqrt of X^2 + y^2 + Z^2.
# multiply by a factor for what constitutes an event we want to log.
# because X, Y, Z are squared acceleration vector is always positive.

print("Calibrating a Baseline")

total_acc_vector = 0
for sample in range(1,baseline_samples):
    x,y,z = accelerometer.acceleration
    total_acc_vector = math.sqrt((x**2)+(y**2)+(z**2)) + total_acc_vector

avg_acc_vector_noise = total_acc_vector/baseline_samples
event_threshold = avg_acc_vector_noise *2
print("\nEvent Threshold:{}\n".format(event_threshold))

# Now we wait for an event greater than the event_threshold.
# if the event occurs then we want to capture data
print ("Wait for Event")

while True:
    x,y,z = accelerometer.acceleration
    if math.sqrt((x**2)+(y**2)+(z**2)) >= event_threshold:
        print("Event Start")
        data_list =[]
        for sample in range (1, max_samples):
#            print(sample)
            x,y,z = accelerometer.acceleration
            data_list.append((x,y,z))
#            print((x,y,z))
            time.sleep(sample_sec)
#    data_list.append(("Collection End:",r.datetime))
#        print(data_list)
        #write out data to SD card.
        with open("/sd/data.txt", "a") as data_file:
            data_file.write("\nTimestamp:{}\n".format(time.monotonic()-power_on_time))
            for line in data_list:
                data_file.write(f"{line}\n")
            data_file.write("Timestamp:{}\n".format(time.monotonic()-power_on_time))
            data_file.close()
        del data_list
        print(gc.mem_free())
        gc.collect()
        print(gc.mem_free())
        print("Event End")
