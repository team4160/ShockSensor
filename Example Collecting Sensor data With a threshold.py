import board
import busio
import digitalio
import time
import adafruit_adxl37x
from adafruit_adxl34x import DataRate
import math
import gc


#settings
samples_per_sec = 32
sample_sec = 1/samples_per_sec
baseline_samples = 32
max_samples = 60



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
        print(data_list)       
        del data_list
        print(gc.mem_free())
        gc.collect()
        print(gc.mem_free())
        print("Event End")
