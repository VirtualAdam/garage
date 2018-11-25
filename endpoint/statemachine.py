import time
import subprocess
import serial
import sys
import time
import datetime

def matrixwritecommand(commandlist): #LCD setup
    commandlist.insert(0, 0xFE)
    for i in range(0, len(commandlist)):
         port.write(chr(commandlist[i]))

def outletred_on(): #outlet 1
    data = subprocess.Popen(["/var/www/rfoutlet/codesend", "1332531", "-p", "3"], stdout=subprocess.PIPE).communicate()[0]
    return

def outletred_off(): #outlet 1
    data = subprocess.Popen(["/var/www/rfoutlet/codesend", "1332540", "-p", "3"], stdout=subprocess.PIPE).communicate()[0]
    return

def outletgreen_on(): #outlet 2
    data = subprocess.Popen(["/var/www/rfoutlet/codesend", "1332675", "-p", "3"], stdout=subprocess.PIPE).communicate()[0]
    return

def outletgreen_off(): #outlet 2
    data = subprocess.Popen(["/var/www/rfoutlet/codesend", "1332684", "-p", "3"], stdout=subprocess.PIPE).communicate()[0]
    return

def distance():
    data = subprocess.Popen(["python", "distance.py"], stdout=subprocess.PIPE).communicate()[0]
    fix = data[:-1]
    num = float(fix)
    inch = convert_to_inches(num)
    return inch

def tester(count):
    time.sleep(.5)
    if count > 0:
        a = count - 5
    else:
        a = count + 100
    return a

def convert_to_inches(input):
    output = input/2.54
    return output

def state1():
    statename="parked"
    #matrixwritecommand([0x99, 180])  # backlight on
    #matrixwritecommand([0xD0, 255, 0, 0])  # backlight red
    outletgreen_off()
    outletred_on()
    timer_start = time.time()
    return statename

def state2():
    statename="Car moving"
    #matrixwritecommand([0x99, 180])  # backlight on
    #matrixwritecommand([0xD0, 0, 255, 0])  # backlight green
    outletgreen_on()
    outletred_off()
    return statename

def state3():
    statename="Door closed"
    #matrixwritecommand([0x99, 180])  # backlight on
    #matrixwritecommand([0xD0, 255, 255, 255])  # backlight white
    outletgreen_off()
    outletred_off()
    return statename

def state4():
    statename="Door open"
    #matrixwritecommand([0x99, 0])  # backlight off
    #matrixwritecommand([0xD0, 255, 255, 255])  # backlight white
    outletgreen_off()
    outletred_off()
    return statename

def state5():
    statename="home"
    outletred_off()
    outletgreen_off()
    return

#Varriables
#port = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=3.0)
state = 0
newstate = 10
timer = 0
timer_start = 0
count = 100
#Main
while True:
    dist = distance()
    #dist = tester(count)
    #count = dist #also for testing
    print dist

    if dist <= 12:
        #print "park it"
        state = 1
    elif dist >12 and dist < 40:
        #car moving
        state = 2
    elif dist >=40 and dist <240:
        #print "door closed"
        state = 3
    else:
        #print "door open"
        state = 4

    if newstate != state:
        newstate = state
        if state == 1:
            timer_start = time.time()
            print state1()
        elif state == 2:
            timer_start = time.time()
            print state2()
        elif state == 3:
            timer_start = 0
            print state3()
        elif state == 4:
            timer_start = 0
            print state4()

    deltime = time.time() - timer_start
    if deltime < 1000000:
        if deltime > 60:
            print "welcome"
            state5()


