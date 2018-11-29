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
        publish.single("lex/garage1/", "garage full", hostname=gatewayip, qos=0) 

    def on_leave(self):
        publish.single("lex/garage1/", "garage empty", hostname=gatewayip, qos=0)

def distance():
    data = subprocess.Popen(["python", "/home/pi/distance.py"], stdout=subprocess.PIPE).communicate()[0]
    fix = data[:-1]
    num = float(fix)
    inch = convert_to_inches(num)
    return inch

def convert_to_inches(input):
    output = input/2.54
    return output   
    
#=========
#main
ip_address = boot.find_ip
gatewayip = boot.find_gateway(ip_address,"yeti")
GarageStatus = GarSensorMachine()

while True:
    print GarageStatus.current_state
    print "enter distance"
    #distraw = raw_input()
    
    dist = int(distraw)
    #motion = run_motion_sensor()
    #if motion == true:
     #   dist= distance.getdistance
    if dist > 30 and GarageStatus.is_empty:
        print "do nothing"   
    elif dist < 30 and GarageStatus.is_empty:
        GarageStatus.arrive()
    elif dist < 30 and GarageStatus.is_full:
        print "nada"
    elif dist > 30 and GarageStatus.is_full:
        GarageStatus.leave()
    time.sleep(2)
    



