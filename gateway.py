#gateway.py
# hostname must be set to lex-nci-gateway
# autostart should also be turned on in /etc/rc.local with the following code before the exit 0:
# sleep 10
#sudo python gateway.py &

import paho.mqtt.client as mqtt
import socket
import sys
import csv
import os
import time
import datetime
import paho.mqtt.publish as publish
from Crypto.Cipher import AES

#=======================
# variables
gateway = "yes"
ip1 = None
blacklist = [None]
ID = []

#=============================
# find local ip address
def find_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    ip = (s.getsockname()[0])
    s.close()
    return ip

#==========================================
def write_csv(filename,results):
    with open(filename, 'w') as csvfile:
        fieldnames = ['topic', 'message']
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(results)

def add_to_results(single):
    # write the file if needed
    if not os.path.exists("sensorlog.txt"):
        flag = 'w'
        print "first time"
    else:
        flag = 'a'
    fo = open("sensorlog.txt", flag)
    fo.write(single)
    fo.close()

#==================================
#subcribe to own broker
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("#", 1)

def on_message_garage(client, userdata, msg):
    print("forward: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    messagestr = msg.topic + "," + msg.payload
    if msg.payload == 'home':
        print "woohoo"
        output = \
        subprocess.Popen(['omxplayer', '-o', 'local', '/home/pi/Fidelity.mp3'], stdout=subprocess.PIPE).communicate()[0]
    add_to_results(messagestr)

def on_message_keepalive(client, userdata, msg):
    top=msg.payload
    #dont do anything

#============================================
#Handler for all sensor messages: forward all messages to the cloud server
def on_message(client, userdata, msg):
    message = msg.payload.decode('UTF-8')
    top = msg.topic.decode('UTF-8')
    topic_parts = top.split('/')
    #print("keepalive: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
            # lex/customer_id/gateway_id/thing_id/datatype/ timestamp data


#boot
localip = find_ip()
print localip
print "booted"

#connect to own broker; loop forevery
client = mqtt.Client()
client.on_connect = on_connect
client.message_callback_add("lex/#", on_message_garage)
client.message_callback_add("axt/#", on_message_keepalive)
client.on_message = on_message
client.subscribe("#", 0)
client.connect(localip, 1883, 60)
#client.loop_forever()

while True:
    rc = client.loop(1)
    time.sleep(1)
    #name = raw_input("continue?")
    #if name == "y":
    publish.single("atx/", "keepalive", hostname=localip, qos=1)
    #else:
    #    publish.single("atx/", "reboot yall", hostname=localip, qos=1)



print "test"