import socket, optparse

parser = optparse.OptionParser()
# parser.add_option('-i', dest='ip', default='10.0.3.40')
parser.add_option('-i', dest='ip', default='239.255.2.0')
parser.add_option('-p', dest='port', type='int', default=12345)
parser.add_option('-m', dest='msg')
(options, args) = parser.parse_args()

print(options.msg)
print(options.ip)
print(options.port)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# enable multicast
s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 3)

s.sendto(options.msg.encode(), (options.ip, options.port) )




#print("send one udp packet")

# python client.py -m "test1"
# 239.255.2.0
# 10.0.3.40


# smcroutectl add eth0 192.168.2.42 255.1.2.3 eth1 eth2
# smcroute -a  10.0.1.10 239.255.2.0 s1-eth3
# smcroutectl add eth0 192.168.2.42 255.1.2.3
# smcroute -a s1-eth1 10.0.1.10 239.255.2.0 s1-eth3