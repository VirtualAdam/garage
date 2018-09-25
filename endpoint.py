# endpoint.py
import subprocess
import socket
import sys
import paho.mqtt.client as mqtt
import datetime
from Crypto.Cipher import AES
import base64
import paho.mqtt.publish as publish
import time
import serial
import nmap

#Varriables=============================

IV = 'This is an IV456'
gateway = "no"
localip = None
iplist = [];
sensorlist = [];
datatype =""
ID = []
myid = "garage1"

gatewayip = None;
gatewayURI = None;
gatewayes = None;

config = [30]  # variable tuple defalt sleeptime 1 minute
shadow = ["sleeptime"]  # topic of variable tuple, default sleeptime
mqttc = mqtt.Client() #needs to be global

outlet1_on = 1332531
outlet1_off = 1332540
outlet2_on = 1332675
outlet2_off = 1332684
outlet3_on = 1332995
outlet3_off = 1333004
outlet4_on = 1334531
outlet4_off = 1334540
outlet5_on = 1340675
outlet5_off = 1340684
#port = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=3.0)
state = 0
newstate = 10
timer = 0
timer_start = 0
count = 100
home = 0
switch = 1

# ================================
# find local ip address
def find_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    ip = (s.getsockname()[0])
    print ip
    s.close()
    return ip

def find_gateway():
    output = subprocess.Popen(["host", "server1"], stdout=subprocess.PIPE).communicate()[0]
    out = output.split()
    print output
    if out[3] == "found:" or "198.105.244.228":
        nm = nmap.PortScanner()
        results = nm.scan('192.168.1.*', '1883')
        for item in results['scan']:
            if item == localip:
                print "just me"
            else:
                if results['scan'][item]['tcp'][1883]['state'] == 'open':
                    out[3] = item
                    print out[3]
    return out[3]

#================================================
#LCD boot
def matrixwritecommand(commandlist):
    commandlist.insert(0, 0xFE)
    for i in range(0, len(commandlist)):
         port.write(chr(commandlist[i]))

# ========================================================
# recieve gateway info from local broker. Only time local broker is used
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # subscription to discovery service, device ID wildcard
    client.subscribe("lex/#", 1)

def boot():
    gatewayip = None
    while gatewayip == None:  # if no brokers exists
        global localip
        localip = find_ip()
        #port.write(localip)
        global gatewayip
        gatewayip = find_gateway()
        print "gateway set: " + str(gatewayip)  # debug
    mes = localip+ " " +myid
    publish.single("lex/boot", mes, hostname=gatewayip, qos=1)
    try:
#        data = subprocess.Popen(["python", "/home/pi/watchdog.py", "$"], stdout=subprocess.PIPE).communicate()[0]
        data = subprocess.Popen(["python", "/home/pi/watchdog.py", "$"], stdout=subprocess.PIPE)
        out = data.stout.readlines()
    except:

        print "oh well"
    print "sensor online"


# ===========================================================
# sensor handler and publish

def smartoutlet(code): #outlet 1
    data = subprocess.Popen(["/var/www/rfoutlet/codesend", str(code), "-p", "3"], stdout=subprocess.PIPE).communicate()[0]
    return

def distance():
    data = subprocess.Popen(["python", "/home/pi/distance.py"], stdout=subprocess.PIPE).communicate()[0]
    fix = data[:-1]
    num = float(fix)
    inch = convert_to_inches(num)
    return inch

def tester(count):
    time.sleep(.5)
    if count > 0 and count < 150:
        a = count -5 * switch
    elif count == 0:
        global switch
        switch = -1
        time.sleep(30)
        a = count - 5 * switch
    elif count >= 150:
        global switch
        switch = 1
        a = count - 5 * switch
    return a

def convert_to_inches(input):
    output = input/2.54
    return output

def state1():
    statename="parked"
    #matrixwritecommand([0x99, 180])  # backlight on
    #matrixwritecommand([0xD0, 255, 0, 0])  # backlight red
    smartoutlet(outlet2_off)
    smartoutlet(outlet1_on)
    global timer_start
    timer_start = time.time()
    publish.single("lex/garage1/", statename, hostname=gatewayip, qos=1)
    return statename

def state2():
    statename="Car moving"
    #matrixwritecommand([0x99, 180])  # backlight on
    #matrixwritecommand([0xD0, 0, 255, 0])  # backlight green
    smartoutlet(outlet2_on)
    smartoutlet(outlet1_off)
    global timer_start
    timer_start = time.time()
    publish.single("lex/garage1/", statename, hostname=gatewayip, qos=1)
    return statename

def state3():
    statename="Door closed"
    #matrixwritecommand([0x99, 180])  # backlight on
    #matrixwritecommand([0xD0, 255, 255, 255])  # backlight white
    smartoutlet(outlet1_off)
    smartoutlet(outlet2_off)
    publish.single("lex/garage1/", statename, hostname=gatewayip, qos=1)
    return statename

def state4():
    statename="Door open"
    #matrixwritecommand([0x99, 0])  # backlight off
    #matrixwritecommand([0xD0, 255, 255, 255])  # backlight white
    smartoutlet(outlet2_off)
    smartoutlet(outlet1_off)
    publish.single("lex/garage1/", statename, hostname=gatewayip, qos=1)
    return statename

def state5():
    statename="home"
    smartoutlet(outlet1_off)
    smartoutlet(outlet2_off)
    publish.single("lex/garage1/", statename, hostname=gatewayip, qos=1)
    return


#Main
boot()

while True:
    dist = distance()
    #dist = tester(count)
    #count = dist #also for testing
    print dist

    if dist <= 12 and home == 0:
        #print "park it"
        state = 1
    elif dist >12 and dist < 40 and home ==0:
        #car moving
        state = 2
    elif dist >=40 and dist <120:
        #print "door closed"
        state = 3
        home = 0
    elif dist > 120:
        #print "door open"
        state = 4
        home = 0
    elif home == 1:
        state = 5

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
        elif state == 5:
            print state5()

    deltime = time.time() - timer_start
    if deltime < 1000000:
        if deltime > 60:
            print "welcome"
            home = 1


#run path
#port = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=3.0) #turn on LCD
#matrixwritecommand([0x58]) #clear LCD


#crypt_out = encrpyt(mykey, sensor()) # runs sensor, encripts it
#print crypt_out


#publish.single("lex/"+str(myid)+"/"+URI, sensor(), hostname=gatewayip, qos=1)
#print "sensor published"


