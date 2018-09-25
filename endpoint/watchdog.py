#!/usr/bin/python

import sys
import time
import paho.mqtt.client as mqtt
import subprocess
import subprocess
import socket
import sys
import paho.mqtt.client as mqtt
import datetime
from Crypto.Cipher import AES
import paho.mqtt.publish as publish
import time
import os
import nmap


# =============================
# Variables
localip = None
datatype =""
ID = []
gatewayip = None
config = [30]  # variable tuple defalt sleeptime 1 minute
shadow = ["sleeptime"]  # topic of variable tuple, default sleeptime
count = 0
#define path
dirname, filename = os.path.split(os.path.abspath(__file__))
print "dir "+dirname


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

def boot():
    gatewayip = None
    while gatewayip == None:  # if no brokers exists
        global localip
        localip = find_ip()
        global gatewayip
        gatewayip = find_gateway()
        print "gateway set: " + str(gatewayip)  # debug
        publish.single("lex/garage1/", "watchdog online", hostname=gatewayip, qos=0)
    print "watchdog online"

def on_connect(mqttc, obj, flags, rc):
    print "Connected to %s:%s" % (mqttc._host, mqttc._port)

def on_message(mqttc, obj, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    global count
    count = 0
#    publish.single("lex/garage1/", "watchdog working", hostname=gatewayip, qos=0)
    if str(msg.payload) == "reboot yall":
        reboot()

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

def reboot():
    print "boom"
    global count
    count = 0
    subprocess.call(['reboot'])

boot()

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
#mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
#mqttc.on_log = on_log
mqttc.connect(gatewayip,1883, 60)
mqttc.subscribe("atx/#", 1)


rc = 0
while rc == 0:
    rc = mqttc.loop(1)
    time.sleep(1)
    count = count +1
    print "count" +str(count)
    if count == 20:
        reboot()
        count = 0
print("rc: "+str(rc))