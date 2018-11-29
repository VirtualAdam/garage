import socket
import nmap
import subprocess

def find_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    ip = (s.getsockname()[0])
    print ip
    s.close()
    return ip


def find_gateway(local_ip, server):
    output = subprocess.Popen(["host", server], stdout=subprocess.PIPE).communicate()[0]
    out = output.split()
    print output
    if out[3] == "found:" or "198.105.244.228":
        nm = nmap.PortScanner()
        results = nm.scan('192.168.1.1-40', '1883')
        for item in results['scan']:
            if item == local_ip:
                print "just me"
            else:
                if results['scan'][item]['tcp'][1883]['state'] == 'open':
                    out[3] = item
                    #print out[3]
    return out[3]

#ip = find_ip()
#gateway = findGateway(ip, "yeti")
#print gateway
