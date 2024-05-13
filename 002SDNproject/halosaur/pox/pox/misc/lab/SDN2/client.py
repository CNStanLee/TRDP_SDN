import socket, optparse, time, struct
# time interval define
delay_ms = 1000
delay_s = 1
# data format define
fmt_uint32 = ">I"
fmt_uint16 = ">H"
fmt_uint8 = ">B"
fmt_string = "{0}s"

# parse the input arguments
parser = optparse.OptionParser()
parser.add_option('-i', dest='ip', default='239.255.2.0')
parser.add_option('-p', dest='port', type='int', default=12345)
parser.add_option('-m', dest='msg')
parser.add_option('-t', dest='interval', type='int', default=30)
(options, args) = parser.parse_args()
# check the input arguments
print(options.msg)
print(options.ip)
print(options.port)
print(options.interval)
# define message content
# seq_counter = 1
# protocol_version = "1.0"
# msg_type = "Test"
# com_id = 123
# etb_topo_count = 0xABCDEF
# op_trn_topo_count = 0x123456
# dataset_length = 100
# reserved = 0xDEADBEEF
# reply_com_id = 456
# reply_ip = "192.168.1.1"
# header_fcs = 0xABCDEF
# data = "Hello, World!"
# # construct the message
# seq_counter = struct.pack(fmt_uint32, seq_counter)
# protocol_version = protocol_version.encode()
# msg_type = msg_type.encode()
# com_id = struct.pack(fmt_uint32, com_id)
# etb_topo_count = struct.pack(fmt_uint32, etb_topo_count)
# op_trn_topo_count = struct.pack(fmt_uint32, op_trn_topo_count)
# dataset_length = struct.pack(fmt_uint32, dataset_length)
# reserved = struct.pack(fmt_uint32, reserved)
# reply_com_id = struct.pack(fmt_uint32, reply_com_id)
# reply_ip = reply_ip.encode()
# header_fcs = struct.pack(fmt_uint32, header_fcs)
# data = data.encode()

# set up the socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 3)

# try:
while True:
    s.sendto(options.msg.encode(), (options.ip, options.port) )
    time.sleep(options.interval/delay_s)
# except KeyboardInterrupt:
#     print("KeyboardInterrupt")
#     s.close()
#     print("Socket closed")
#     exit(0)




#print("send one udp packet")

# python client.py -m "test1"
# 239.255.2.0
# 10.0.3.40


# smcroutectl add eth0 192.168.2.42 255.1.2.3 eth1 eth2
# smcroute -a  10.0.1.10 239.255.2.0 s1-eth3
# smcroutectl add eth0 192.168.2.42 255.1.2.3
# smcroute -a s1-eth1 10.0.1.10 239.255.2.0 s1-eth3