
import uuid
import subprocess
import time

def take_picture():
	filename = uuid.uuid4().hex
	fullname = filename+".jpg"
	data = subprocess.Popen(["fswebcam", fullname], stdout=subprocess.PIPE).communicate()[0]
	return fullname
	
def send_pic_to_server(filename, server):
	files = "file=@/home/pi/Superman/"+filename
	print files
	data = subprocess.Popen(["curl", "-X", "POST", "-F", "file=@/home/pi/Superman/"+filename, server], stdout=subprocess.PIPE).communicate()[0]
	#sudo curl -X POST -F file=@/home/pi/Superman/image.jpg http://localhost:8000
'''
server_id = "http://localhost:8000"
picture_id = take_picture()
print picture_id
time.sleep(2)
send_pic_to_server(picture_id, server_id)
'''
