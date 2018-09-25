'''
/*
 * Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import getopt
import paho.mqtt.client as mqtt
import socket
import sys
import time
import datetime
import paho.mqtt.publish as publish
from Crypto.Cipher import AES

#=======================
# variables

# Read in command-line parameters
#useWebsocket = False
#host = "a15kflar0t106y.iot.us-west-2.amazonaws.com"
#rootCAPath = "/home/pi/gateway/aws-iot-device-sdk-python/certs/root-CA.crt"
#certificatePath = "/home/pi/gateway/aws-iot-device-sdk-python/certs/a3b1a279e6-certificate.pem.crt"
#privateKeyPath = "/home/pi/gateway/aws-iot-device-sdk-python/certs/a3b1a279e6-private.pem.key"
#customer_id = "giRC5IkH7z0t"
#store_id = "71f3cc16-9df2-4fc1-929b-6b49372a87b8"
#clientname = "adam-aws-gateway"

# Configure logging
logger = None
if sys.version_info[0] == 3:
	logger = logging.getLogger("core")  # Python 3
else:
	logger = logging.getLogger("AWSIoTPythonSDK.core")  # Python 2
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

ID = []
with open('/home/pi/certs/gateway_id.txt', 'r') as f:
    for line in f:
        ID.append(line)
    f.close()
host = ID[0][:-1]
rootCAPath = ID[1][:-1]
certificatePath = ID[2][:-1]
privateKeyPath = ID[3][:-1]
customer_id = ID[4][:-1]
store_id = ID[5][:-1]
clientname = ID[6][:-1]

print host
print rootCAPath
print certificatePath
print privateKeyPath
print customer_id
print store_id
print clientname

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientname)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Custom MQTT message callback
def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")

#=============================
# find local ip address
def find_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    ip = (s.getsockname()[0])
    s.close()
    return ip

#==================================
#subcribe to own broker
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("#", 1)

#============================================
#Handler for all sensor messages: forward all messages to the cloud server
def on_message(client, userdata, msg):
    message = msg.payload.decode('UTF-8')
    top = msg.topic.decode('UTF-8')
    topic_parts = top.split('/')
    x = str(topic_parts[1])
    y = str(msg.payload)
    if (topic_parts[0] == "lex"):
        if (x,y) in blacklist:
            print "blacklist"
        else:
            myAWSIoTMQTTClient.publish("lex/"+customer_id+"/"+store_id+"/"+topic_parts[1]+"/"+topic_parts[2], msg.payload, 1)
            print("forward: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
            # lex/customer_id/gateway_id/thing_id/datatype/ timestamp data

#boot
localip = find_ip()
print localip
# Connect and subscribe to AWS IoT
print "got here"
#myAWSIoTMQTTClient.connect()
print "got here too"
#myAWSIoTMQTTClient.subscribe("test/shadow", 1, customCallback)
time.sleep(2)


#connect to own broker; loop forevery
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.subscribe("#", 0)
client.connect(localip, 1883, 60)
client.loop_forever()






