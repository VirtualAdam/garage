'''file still not working.  AttributeError: 'module' object has no attribute 'find_gateway'

'''
#!/usr/bin/python
import os, sys, inspect
# use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"common")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from common import boot
import subprocess
import socket
import datetime
import time

#Varriables=============================



# ================================
# find local ip address
def find_ip():
    ip = boot.find_ip()
    return ip

def find_gateway(local_ip,server):
    gateway = boot.findGateway(local_ip, server)
    return gateway


#Main
localip = find_ip()
print localip
gateway = find_gateway(localip,"server1")
print gateway



