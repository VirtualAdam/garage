# endpoint.py

'''
from common import distance.distance as distance

import subprocess
import socket
import sys
import paho.mqtt.client as mqtt
import datetime
from Crypto.Cipher import AES
import base64
import paho.mqtt.publish as publish

import serial
import nmap
'''
from statemachine import StateMachine, State
import time
import paho.mqtt.publish as publish
from common import boot
from sensor import distance
import camera
server_id = "http://192.168.1.35:8040"


class GarSensorMachine(StateMachine):
    #states
    empty = State('Empty', initial=True)
    full = State('Full')

    #transistions
    arrive = empty.to(full)
    leave = full.to(empty)
    
    #callbacks

    def on_arrive(self):
        print('howdy') 
        picture_id = camera.take_picture()
        time.sleep(2)
        camera.send_pic_to_server(picture_id, server_id)  
        publish.single("lex/garage1/", "garage full-"+picture_id, hostname=gatewayip, qos=0) 
        time.sleep(3)
        camera.delete_pic_on_disk(picture_id)

    def on_leave(self):
        print('see ya') 
        picture_id = camera.take_picture()
        time.sleep(2)
        camera.send_pic_to_server(picture_id, server_id)  
        publish.single("lex/garage1/", "garage empty-"+picture_id, hostname=gatewayip, qos=0) 
        time.sleep(3)
        camera.delete_pic_on_disk(picture_id)

#=========
#main
ip_address = boot.find_ip()
print "my ip is "+str(ip_address)
gatelist = boot.find_gateway(ip_address, "yeti")
print gatelist
gatewayip = boot.check_address(gatelist)
print "gateway is "+str(gatewayip)
GarageStatus = GarSensorMachine()

while True:
    print GarageStatus.current_state
    dist1 = distance.getdistance()
    print "d1 "+str(dist1)
    time.sleep(2)
    dist2 = distance.getdistance()
    print "d2 "+str(dist2)
    time.sleep(2)
    dist3 = distance.getdistance()
    print "d3 "+str(dist3)
    if dist1 == dist2 and dist2 == dist3:
        dist = dist1
        if dist > 25 and GarageStatus.is_empty:
            print "do nothing"   
        elif dist < 25 and GarageStatus.is_empty:
            GarageStatus.arrive()
        elif dist < 25 and GarageStatus.is_full:
            print "nada"
        elif dist > 25 and GarageStatus.is_full:
            GarageStatus.leave()
    time.sleep(60)
    



