import board
import busio
import time
import adafruit_adxl37x
from adafruit_adxl34x import DataRate

i2c = busio.I2C(scl=board.GP21, sda=board.GP20)  # Set and define where SCL and SDA are connected.
global accelerometer
accelerometer = adafruit_adxl37x.ADXL375(i2c)
accelerometer.data_rate  = DataRate.RATE_800_HZ

_REG_DATA_FORMAT: int = 0x31

#_INT_ACT: int = 0b00010000

#so this maybe?
active_change = accelerometer._read_register_unpacked(_REG_DATA_FORMAT)
#accelerometer._write_resgiter_byte(_REG_INT_ENABLE, 0x0) #disables interrupts, so that we can write new things to registers without messing other things up?
#accelerometer._write_register_byte(_REG_DATA_FORMAT, 0b00001011) #0b00001011 comes from the adafruit arduino library linked by ty which supposedly fixes the bits at _reg_data_format for 25+ g
#accelerometer._write_register_byte(_REG_DATA_FORMAT, _INT_ACT) # ACT bit
#active_change |= _INT_ACT
accelerometer._write_register_byte(_REG_DATA_FORMAT, active_change | 0b00001011) #0b00001011 comes from the adafruit arduino library linked by ty which supposedly fixes the bits at _reg_data_format for 25+ g
# playing around with sampling rates. 64 works.
samples_per_sec = 64
sample_sec = 1/samples_per_sec

while True:
    x,y,z = accelerometer.acceleration
    print((x,y,z))
    time.sleep(sample_sec)
