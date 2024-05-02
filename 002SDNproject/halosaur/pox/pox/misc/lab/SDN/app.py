'''
Author: Changhongli lic9@tcd.com
Date: 2024-04-28 19:50:47
LastEditors: Changhongli lic9@tcd.com
LastEditTime: 2024-04-28 20:02:14
FilePath: /pox/pox/misc/lab/SDN/app.py
Description: 

'''
import socket
import time
import sys
import random

if len(sys.argv) != 3:
    print("Usage: {} <destination_ip> <send_period_seconds>".format(sys.argv[0]))
    sys.exit(1)
    
destination_ip = sys.argv[1]
send_period = int(sys.argv[2])

destination_port = random.randint(1024, 65535)

# create udp socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# use random port
sock.bind(('', 0))
# get local port
local_port = sock.getsockname()[1]

print("Starting to send UDP packets from port {} to {}:{}".format(local_port, destination_ip, destination_port))


while True:
    message = b'Hello, UDP!'
    sock.sendto(message, (destination_ip, destination_port))
    print("Sent UDP packet from port {} to {}:{}".format(local_port, destination_ip, destination_port))
    time.sleep(send_period/1000)