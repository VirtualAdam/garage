

import serial
import sys
import time


ROWS = 2
COLS = 16

def matrixwritecommand(commandlist):
    commandlist.insert(0, 0xFE)
    for i in range(0, len(commandlist)):
         port.write(chr(commandlist[i]))


port = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=3.0)
matrixwritecommand([0x58])
matrixwritecommand([0x99, 0])#backlight off
port.write("ehello world")
time.sleep(5)
matrixwritecommand([0x58])
port.write("most test")
time.sleep(3)
matrixwritecommand([0x58])#clear display
matrixwritecommand([0x99, 255])#backlight on
time.sleep(1)
matrixwritecommand([0x99, 0])#backlight off
