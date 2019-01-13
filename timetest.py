import subprocess
from common import boot


ip_address = boot.find_ip()
print "my ip is "+str(ip_address)
gatelist = boot.find_gateway(ip_address, "yeti")
print gatelist
gateway = boot.check_address(gatelist)
print "my gateway is "+str(gateway)
