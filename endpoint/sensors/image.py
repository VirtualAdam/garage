#image.py
import subprocess
import os
import socket
import sys
import paho.mqtt.client as mqtt
import fcntl
import struct
import time
import paho.mqtt.publish as publish
import random
import subprocess
import random
import urllib
import urllib2
import json
import requests
import sys
import time
import os



DATATABLES_URL = 'https://datatables-staging.iss.lxk.co'
PRODUCT_DATABASE_ID = "witjjl7HcgRd"
IMAGES_TABLE_ID = 'table:RqmHnk02uwvo'
IDP_URL = 'https://idp-staging.psft.co/oauth/token'
# IDP_URL = 'http://localhost:3000/oauth/token'
CLIENT_ID = 'datatables-python'
CLIENT_SECRET = '4b8c9101ff2c8baccd86116aef3cb97d03381ebdb42564379d4377d59613515a'

# ===========================================================
# sensor handler and publish
def sensor():
    photoID = random.getrandbits(64)
    subprocess.check_output(['fswebcam', '--no-banner', '/home/pi/data/' + str(photoID) + '.jpg'])
    time.sleep(1)
#    print "uploading file: " + str(photoID)
    body = {
        "client_id": "datatables-python",
        "client_secret": "4b8c9101ff2c8baccd86116aef3cb97d03381ebdb42564379d4377d59613515a",
        "grant_type": "client_credentials"
    }
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    r = requests.post(IDP_URL, data=json.dumps(body), headers=headers)
    resp = json.loads(r.text)
    access_token = resp['access_token']
#    print "Got access token: " + access_token
    token_string = 'Bearer ' + access_token

    upload_file_name = str(photoID) + ".jpg"

    request_url = DATATABLES_URL + '/databases/' + PRODUCT_DATABASE_ID + '/tables/' + IMAGES_TABLE_ID + '/rows'
    r = requests.post(request_url, data={'ImageID': upload_file_name},
                      headers={'Authorization': token_string})
    row_id = r.json()['id']
    request_url = request_url + '/' + row_id + '/upload?column=' + 'file'
    r = requests.post(request_url, headers={'Authorization': token_string},
                      files={'file': open("data/" + upload_file_name, 'rb')})
#    print "upload returned: " + str(r.status_code)
    if r.status_code == 200:
        os.remove("data/" + upload_file_name)
#    else:
#        print "Failed to upload: " + str(photoID)
    output = str(photoID)
    print output

sensor()





