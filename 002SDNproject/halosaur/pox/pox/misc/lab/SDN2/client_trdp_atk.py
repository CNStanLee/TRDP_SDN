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

import socket, optparse, time, struct, random
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
dataset_length = options.dataset_length - 82  # offset 82 bytes
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


# if data_tag is 4, then the node is disabled
# exit the program
if options.data_tag == 4:
    exit()

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

# random factor for the delay time, 10% of the delay time
random_factor_normal = 0.01
# random_factor_atk1 = 0.2
random_factor_atk1 = 0.6

# the random factor that in use
# initialize the random factor as a normal offset
random_factor_inuse = random_factor_normal

# set atk flag
atk_flag = 0

# origin delay time
delay_ori = options.interval

# get the system time
start_time = time.time()

# if the message is loop, then keep sending the message
while options.loop == 1:
    # add some random factor to the delay_time
    
    if atk_flag == 0:
        # normal send
        random_factor_inuse = random_factor_normal
        delay_with_random = delay_ori + (delay_ori * random_factor_inuse * (random.random() - 0.5))
    elif atk_flag == 1:
        # use attack strategy 1
        random_factor_inuse = random_factor_atk1
        delay_with_random = delay_ori + (delay_ori * random_factor_inuse * (random.random() - 0.5))
    elif atk_flag == 2:
        # use attack strategy 2
        # dos attack
        # delay_with_random = 5
        delay_with_random = 3
    elif atk_flag == 3:
        # use attack strategy 3
        # randomly generate a number from 10 to 100
        # delay_with_random = random.randint(10, 100)
        # delay_with_random = random.randint(10, 300)
        # delay_with_random = random.randint(1, 300)
        delay_with_random = random.randint(28, 71)

    # wait for the time interval
    time.sleep(delay_with_random/delay_ms)
    # update sequence counter
    seq_counter_ori = seq_counter_ori + 1
    seq_counter = struct.pack(fmt_uint32, seq_counter_ori) 
    # construct the message
    # msg = seq_counter + protocol_version_msg_type + \
    #   com_id + etb_topo_count + op_trn_topo_count + \
    #   dataset_length + reserved + \
    #   reply_com_id + reply_ip + \
    #   header_fcs + data_tag + data_content
    atk_flag_f = struct.pack(fmt_uint32, atk_flag)

    msg = seq_counter + protocol_version_msg_type + \
      com_id + etb_topo_count + op_trn_topo_count + \
      dataset_length + reserved + \
      reply_com_id + reply_ip + \
      header_fcs + atk_flag_f + data_content
    # mark as atk message only when the attack is ex
    # send the message
    s.sendto(msg, (options.ip, options.port))
    # check the time
    current_time = time.time()
    # if the time is more than 10 seconds, then change the random factor
    #running_time = current_time - start_time
    
    # every 5 seconds, change the attack strategy

    # if options.data_tag == 1:
    #     # atk1
    #     if 20 < running_time <= 50:
    #         atk_flag = 1
    #     elif 50 < running_time <= 100 :
    #         atk_flag = 0
    #     elif 100 < running_time <= 130:
    #         atk_flag = 0
    #     elif 130 < running_time <= 170:
    #         atk_flag = 0
    #     elif 170 < running_time <= 200:
    #         atk_flag = 0
    #     else: 
    #         atk_flag = 0

    # if options.data_tag == 2:
    #     # atk2 dos attack
    #     if 20 < running_time <= 50:
    #         atk_flag = 0
    #     elif 50 < running_time <= 100 :
    #         atk_flag = 0
    #     elif 100 < running_time <= 130:
    #         atk_flag = 2
    #     elif 130 < running_time <= 170:
    #         atk_flag = 0
    #     elif 170 < running_time <= 200:
    #         atk_flag = 0
    #     else: 
    #         atk_flag = 0
    
    # if options.data_tag == 3:
    #     # atk3
    #     if 20 < running_time <= 50:
    #         atk_flag = 0
    #     elif 50 < running_time <= 100 :
    #         atk_flag = 0
    #     elif 100 < running_time <= 130:
    #         atk_flag = 0
    #     elif 130 < running_time <= 170:
    #         atk_flag = 0
    #     elif 170 < running_time <= 200:
    #         atk_flag = 3
    #     else: 
    #         atk_flag = 0
    
    # construct atk period
    running_time = current_time - start_time
    if running_time > 30:
        start_time = current_time
        running_time = 0
    
    if 0 < running_time <= 5:
        atk_flag = 0
    elif 5 < running_time <= 10:
        if options.data_tag == 1:
            atk_flag = 1
    elif 10 < running_time <= 15:
        atk_flag = 0
    elif 15 < running_time <= 20:
        if options.data_tag == 2:
            atk_flag = 2
    elif 20 < running_time <= 25:
        atk_flag = 0
    elif 25 < running_time <= 30:
        if options.data_tag == 3:
            atk_flag = 3
    else:
        atk_flag = 0
