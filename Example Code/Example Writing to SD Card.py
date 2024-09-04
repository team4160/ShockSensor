import board
import busio
import sdcardio
import storage
import digitalio

# Use an SPI bus on specific pins:
spi = busio.SPI(board.GP2, MOSI=board.GP3, MISO=board.GP0)
cs = board.GP1


# Create SD CARD
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
    except:
        print("Failed to Mount")

except:
    print("Failed to Mount")

data_list =[(0,0,0)]
data_list.append((1,1,1))

#write out data to SD card.
with open("/sd/data.txt", "a") as data_file:
    data_file.write("Start of Event\n")
    for line in data_list:
        data_file.write(f"{line}\n")
    data_file.write("End of Event\n")
    data_file.close()

print("Done!")
