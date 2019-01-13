import socket
import nmap
import subprocess
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import time
import paho.mqtt.client as mqtt
gate = False
iplist = []

def on_connect(client, userdata, flags, rc):
    #print("Connected with result code " + str(rc))
    client.subscribe("#", 1)

# when receiving a mqtt message do this;

def on_message(client, userdata, msg):
    top = msg.topic.decode('UTF-8')
    topic_parts = top.split('/')
    
def on_message_gateway(client, userdata, msg):
    #print("startup: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    global gate
    gate = msg.payload
    
def loopfun(iptry):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.message_callback_add("gateway/yes/#", on_message_gateway)
    client.on_message = on_message
    client.subscribe("#", 0)
    client.connect(iptry, 1883, 60)
    client.loop_start()
    publish.single("gateway/", "request", hostname=iptry, qos=0)
    time.sleep(3)
    client.loop_stop()

def check_address(iplist):
    for x in iplist:
        global gate
        gate = False
        loopfun(x)
        if gate != False:
           output = gate
           #print "check "+output
    return output

def find_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    ip = (s.getsockname()[0])
    #print ip
    s.close()
    return ip


def find_gateway(local_ip, server):
    output = subprocess.Popen(["host", server], stdout=subprocess.PIPE).communicate()[0]
    out = output.split()
    #print output
    if out[3] == "found:" or "198.105.244.228":
        nm = nmap.PortScanner()
        results = nm.scan('192.168.1.1-40', '1883')
        for item in results['scan']:
            #if item == local_ip:
            #    print "just me"
            #else:
            if results['scan'][item]['tcp'][1883]['state'] == 'open':
                iplist.append(item)
                #out[3] = item
                #print out[3]
    return iplist



