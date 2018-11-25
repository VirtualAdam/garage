#server.py 6/6
import paho.mqtt.client as mqtt
import socket
import sys
import paho.mqtt.publish as publish
import json
import requests
import time
import base64
from Crypto.Cipher import AES
import datetime

#===========================
#config data
#DATATABLES_URL = 'https://datatables-staging.iss.lxk.co'
#PRODUCT_DATABASE_ID = "5PPHzbkW9jzE" #IoT
#TURNTABLE_IMAGES_TABLE_ID = 'table:Hp1zeXtoYX_I'  # IoT ingest
#IDP_URL = 'https://idp-staging.psft.co/oauth/token'
#CLIENT_ID = 'datatables-python'
#CLIENT_SECRET = '4b8c9101ff2c8baccd86116aef3cb97d03381ebdb42564379d4377d59613515a'
#myid = "server101"
#keylist = [("ep101","qwertyuiopasdfg1"),("ep102","qwertyuiopasdfg2"),("endpoint102", "F1FEC586ECC533ABE60247950160350F")]
#serverip = "magic-squirrel.dhcp.ad.rds.lexmark.com" #behind the firewall
#serverip = "52.39.168.117" #AWS broker
#serverip = "10.199.108.79" #RDS not working for some reason

#=======================
# variables
gateway = []
ip1 = None
URI = "server"
blacklist = []
keydict = {}
cID = []

#DATATABLES_URL = 'https://datatables-dev.iss.lxk.co'
#PRODUCT_DATABASE_ID = "7c85539b-0376-4c58-8657-1d1cf7bca23a" #bootdev
#TABLE_ID = '8063853d-b6c0-4996-a868-aa016f3399c6'  # bootable
#IDP_URL = 'https://idp-dev.iss.lxk.co/oauth/token'
#CLIENT_ID = 'noncoreiot'
#CLIENT_SECRET = '55807c62a20d39ccafa0da20d19a87552c7a49af9473c1dc0d6f16ae611e1bc6'

####read server config at serverID.txt
with open('server/serverID.txt', 'r') as f:
    data = f.readlines()
    for line in data:
        cID.append(line)
    f.close()
DATATABLES_URL = cID[0][:-2] #[:-2] is to remove the invisible '/n' for each line
PRODUCT_DATABASE_ID = cID[1][:-2] #IoT
TABLE_ID = cID[2][:-2]  # IoT ingest
IDP_URL = cID[3][:-2]
CLIENT_ID = cID[4][:-2]
CLIENT_SECRET = cID[5][:-2]
myid = cID[6][:-2]
serverip = cID[7][:-2] #aws

print DATATABLES_URL
print TABLE_ID

#load the key dictionary
with open("server/IDmaster.txt") as f:
    for line in f:
       (ID, val) = line.split()
       global keydict
       keydict[ID] = val

#=============================
# find local ip address
def find_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    ip = (s.getsockname()[0])
    print ip
    s.close()
    return ip

#builds string from blacklist tuple this was getting out of sync before, so I added range(0, len back in
def build_string(bernie):
    clint = ""
    for n in range(0, len(bernie)):
        burn = bernie[n]
        hill = burn[0]+"."+burn[1]
        if n == 0:
            clint = hill
        else:
            clint = clint+":"+hill
    return(clint)

#==================================
#subcribe to server broker
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("lex/#",1)

#===============================================
#handler for gateway, checks to see if gateway is already in system, if so it deletes the old record with the old ip
#then adds new record with new ip address.
def on_message_gateway(mosq, obj, msg):
    # This callback will only be called for messages with topics that match gateway/#
    message = msg.payload.decode('UTF-8') #spit topic
    top = msg.topic.decode('UTF-8')
    topic_parts = top.split('/')
    if topic_parts[0] == "gateway":
        temp = (topic_parts[1], msg.payload) #creates a tuple (gateway name, ip_address)
        for n in gateway:
            if topic_parts[1] == n[0]:
                gateway.remove((topic_parts[1],n[1]))
                print "pop"
        global gateway
        gateway.append(temp) #adds tuple to list
        print "gateway"
        print gateway

#============================================
def on_message(client, userdata, msg):
    message = msg.payload.decode('UTF-8')
    top = msg.topic.decode('UTF-8')
    topic_parts = top.split('/')
    print("MESSAGES: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    #lex/customer_id/store_id/thing_id/datatype/ timestamp data
    if topic_parts[0] == "lex":
     #   token = token_lookup(topic_parts[2]) #looks up token with endpointID
     #   data = decrypt(token, msg.payload) # decrypts message
        d = msg.payload.split(" ")
        timestamp = d[0]
        data = d[1:]
        print timestamp
        print data
        new_row(topic_parts[1], topic_parts[2], topic_parts[3], topic_parts[4], timestamp, data) #upload to datatables
        blacklist.append((topic_parts[2], msg.payload))
        print blacklist
        if len(blacklist) > 10: #limits blacklist to 10 items (totally aribtrary number)
            blacklist.pop[0]
            print "blacklist pop"
        string = build_string(blacklist)
        for n in range(0, len(gateway)):
            if topic_parts[0] == gateway[n][0]:
                publish.single("lexmark/"+str(topic_parts[2])+"/"+str(topic_parts[4])+"/blacklist", string, hostname=gateway[n][1], qos=1)

#============================
#decrypt
def decrypt(token, ciphertext):
    newct = base64.b64decode(ciphertext) #convert back from base
    IV = newct[:16]  # Capture IV
    data = newct[16:] # remove IV from message
    obj = AES.new(token, AES.MODE_CBC, IV)  #setup decryption with token and IV
    pad = obj.decrypt(data) # decrypt message
    message = remove_pad(pad)
    return message

#============================
#remove padding for block size
def remove_pad(line):
    padlen = int(line[:16])
    print "padlen " + str(padlen)
    line2 = line[:-padlen]
    line3 = line2[16:]
    return line3

#=======================
#unique key lookup
def token_lookup(endpointID):
    print keydict
    print "endpoint "+ endpointID
    x = keydict[endpointID]
    print x
    return x

#=======================================
#upload for datatables.
def new_row(customer_id, store_id, thing_id, datatype, timestamp, msgdata):
    body = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    r = requests.post(IDP_URL, data=json.dumps(body), headers=headers)
    resp = r.json()
    print resp
    access_token = resp['access_token']
    print "Got access token: " + access_token
    token_string = 'Bearer ' + access_token
    print "Uploading with: " +thing_id + ' ' + str(msgdata)+ ' '
    request_url = DATATABLES_URL + '/databases/' + PRODUCT_DATABASE_ID + '/tables/' + TABLE_ID + '/rows'
    r = requests.post(request_url, data={'store_id':store_id,'customer_id':customer_id, 'thing_id' :thing_id, 'data': str(msgdata), 'datatype':datatype, 'timestamp':timestamp},
                      headers={'Authorization': token_string})
    print "upload returned: " + str(r.status_code)
    if r.status_code == 200:
        print "yay"
    else:
        print "Failed to upload: "

#boot
localip = find_ip()
parts= localip.split('.')
if str(parts[0]) =="157" or "10" or "192":
    print str(parts[0]) + " rds"
    serverip = "magic-squirrel.dhcp.ad.rds.lexmark.com"  # behind the firewall
    print serverip

#connect to own broker; loop forever
print "start mqtt " + serverip
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.message_callback_add("gateway/#", on_message_gateway)
client.subscribe("#", 1)
client.connect(serverip, 1883, 60)
client.loop_forever()