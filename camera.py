import os
import uuid
import subprocess
import time

def take_picture():
	filename = uuid.uuid4().hex
	fullname = filename+".jpg"
	data = subprocess.Popen(["fswebcam", fullname], stdout=subprocess.PIPE).communicate()[0]
	return fullname
	
def send_pic_to_server(filename, server):
	path = os.path.dirname(os.path.abspath(__file__))
	files = "file=@"+path+"/"+filename
	print files
	data = subprocess.Popen(["curl", "-X", "POST", "-F", files, server], stdout=subprocess.PIPE).communicate()[0]
	#sudo curl -X POST -F file=@/home/pi/Superman/image.jpg http://localhost:8000

def delete_pic_on_disk(filename):
	os.remove(filename)
	here = os.path.isfile(filename) 
	print here

'''
server_id = "http://localhost:8000"
picture_id = take_picture()
print picture_id
time.sleep(2)
send_pic_to_server(picture_id, server_id)
time.sleep(3)
delete_pic_on_disk(picture_id)
'''
