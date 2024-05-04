#####################################################
# This is the client side of the TRDP protocol
# The client will send the message to the server
# The demo command is:
# one shot:
# python3 client_trdp.py
# loop:
# python3 client_trdp.py -b broadcast_address
# -p port_number
# -m message
# -t time_interval
# -l loop_flag
# -c com_id
# -d dataset_length
# -a data_tag

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
# broadcast address
parser.add_option('-b', dest='ip', default='239.255.2.0')
# port number
parser.add_option('-p', dest='port', type='int', default=12345)
# specific message
parser.add_option('-m', dest='msg', default='HelloWorld')
# time interval
parser.add_option('-t', dest='interval', type='int', default=30)
# if the message is loop or not
parser.add_option('-l', dest='loop', type='int', default=0)
# get the com id
parser.add_option('-c', dest='com_id', type='int', default=1200)
# get the dataset length
parser.add_option('-d', dest='dataset_length', type='int', default=1400)
# get data type(0 normal, 1 attack)
parser.add_option('-a', dest='data_tag', type='int', default=0)
(options, args) = parser.parse_args()


# define message content
# sequence counter should be incremented by 1 for each message
seq_counter_ori = 0x000314d4
# protocol version and msg type should be fixed value
protocol_version_msg_type = 0x01005064
# input parameters
# com_id = 1200
com_id = options.com_id
# etb_topo_count para is not enabled N/A
etb_topo_count = 0
# para is not enabled N/A
op_trn_topo_count = 0
# input parameters
dataset_length = options.dataset_length
# reserved para
reserved = 0
reply_com_id = 0
reply_ip = 0
# header checksum, simulation use fixed value instead of calculating
header_fcs = 0xAC12CC3C
# data tag, 0 means normal data, otherwise means attack data
data_tag = 0x00000000
data_tag = data_tag + options.data_tag
# data content
# data_content = "Hello, World!"
data_content = options.msg
# use 0x00 to fill the data content to the length of dataset_length
# consider all the head message, the data content should be less than 1400
# minus 40 bytes as the head message
data_content = data_content + '\0'*(dataset_length-len(data_content)-4)


# construct the message
seq_counter = struct.pack(fmt_uint32, seq_counter_ori)
protocol_version_msg_type = struct.pack(fmt_uint32, protocol_version_msg_type)
com_id = struct.pack(fmt_uint32, com_id)
etb_topo_count = struct.pack(fmt_uint32, etb_topo_count)
op_trn_topo_count = struct.pack(fmt_uint32, op_trn_topo_count)
dataset_length = struct.pack(fmt_uint32, dataset_length)
reserved = struct.pack(fmt_uint32, reserved)
reply_com_id = struct.pack(fmt_uint32, reply_com_id)
reply_ip = struct.pack(fmt_uint32, reply_ip)
header_fcs = struct.pack(fmt_uint32, header_fcs)
data_tag = struct.pack(fmt_uint32, data_tag)
data_content = data_content.encode()

# construct the message
msg = seq_counter + protocol_version_msg_type + \
      com_id + etb_topo_count + op_trn_topo_count + \
      dataset_length + reserved + \
      reply_com_id + reply_ip + \
      header_fcs + data_tag + data_content

# set up the socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 3)


# send the message
s.sendto(msg, (options.ip, options.port) )

# if the message is loop, then keep sending the message
while options.loop == 1:
    # wait for the time interval
    time.sleep(options.interval/delay_ms)
    # update sequence counter
    seq_counter_ori = seq_counter_ori + 1
    seq_counter = struct.pack(fmt_uint32, seq_counter_ori) 
    # construct the message
    msg = seq_counter + protocol_version_msg_type + \
      com_id + etb_topo_count + op_trn_topo_count + \
      dataset_length + reserved + \
      reply_com_id + reply_ip + \
      header_fcs + data_tag + data_content
    # send the message
    s.sendto(msg, (options.ip, options.port))
    

