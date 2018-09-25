import subprocess
import time
import os
devices = ["first thing"]
num = 0

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

while True:
    num = num + 1
    output = subprocess.Popen(["hcitool", "scan"], stdout=subprocess.PIPE).communicate()[0]
    time.sleep(5)
    out = output.split()
    print output
    try:
        if out[3] in devices:
            print "gotcha"
        else:
            print out[2]
                #print out[3]
                #print out[4]
            add_to_results(out[3])
            add_to_results(out[4])
            devices.append(out[3])
    except IndexError:
        print "still looking " + str(num)
        print devices


