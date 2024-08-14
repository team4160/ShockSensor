import os
import time
import rtc
import socketpool
import wifi
import adafruit_ntp
 
# Time zone offset in hours from UTC/GMT
# GMT = 0
# PST = -8
# CST = -7
# MST = -6
# EST = -5
 
TZ_OFFSET = -8  
 
# Connect to local network
# Wifi SSID and password are stored in settings.toml file
wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
print("Wifi connected.")
 
# Get current time using NTP
print("Fetching time from NTP.")
pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=TZ_OFFSET, socket_timeout=20)
# set the Pico Clock to NTP time
rtc.RTC().datetime = ntp.datetime
 
 
while True:
    now = time.localtime()
    # Print current time in format hh:mm:ss
    print("Current time: {:2}:{:02}:{:02}".format(now.tm_hour, now.tm_min, now.tm_sec))
    time.sleep(1)
