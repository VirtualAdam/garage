import socket
import fcntl
import struct
import serial
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

address = get_ip_address('eth0')  # '192.168.0.110'

port = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=3.0)
port.write(address)