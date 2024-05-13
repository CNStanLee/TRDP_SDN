'''
Author: Changhongli lic9@tcd.com
Date: 2024-04-09 22:12:43
LastEditors: Changhongli lic9@tcd.com
LastEditTime: 2024-04-28 21:11:03
FilePath: /pox/pox/misc/lab/SDN/controller_trdp.py
Description: 

'''
from pox.core import core
import pox.lib.packet as pkt
import pox.lib.packet.ethernet as eth
import pox.lib.packet.arp as arp
import pox.lib.packet.icmp as icmp
import pox.lib.packet.ipv4 as ip
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr


# ip definition
h11_ip = '10.0.1.10'
h12_ip = '10.0.1.11'
h13_ip = '10.0.1.40'
h14_ip = '10.0.1.41'
h15_ip = '10.0.1.20'
h16_ip = '10.0.1.140'
h17_ip = '10.0.1.210'
h18_ip = '10.0.1.30'
h19_ip = '10.0.1.31'

h21_ip = '10.0.2.40'
h22_ip = '10.0.2.41'
h23_ip = '10.0.2.100'
h24_ip = '10.0.2.120'
h25_ip = '10.0.2.140'

h31_ip = '10.0.2.40'
h32_ip = '10.0.2.41'
h33_ip = '10.0.3.120'
h34_ip = '10.0.3.140'

h41_ip = '10.0.4.40'
h42_ip = '10.0.4.41'
h43_ip = '10.0.4.100'
h44_ip = '10.0.4.120'
h45_ip = '10.0.4.140'

# mac definition
h11_mac = '00:00:00:00:01:10'
h12_mac = '00:00:00:00:01:11'
h13_mac = '00:00:00:00:01:40'
h14_mac = '00:00:00:00:01:41'
h15_mac = '00:00:00:00:01:20'
h16_mac = '00:00:00:00:01:140'
h17_mac = '00:00:00:00:01:210'
h18_mac = '00:00:00:00:01:30'
h19_mac = '00:00:00:00:01:31'

h21_mac = '00:00:00:00:02:40'
h22_mac = '00:00:00:00:02:41'
h23_mac = '00:00:00:00:02:100'
h24_mac = '00:00:00:00:02:120'
h25_mac = '00:00:00:00:02:140'

h31_mac = '00:00:00:00:03:40'
h32_mac = '00:00:00:00:03:41'
h33_mac = '00:00:00:00:03:120'
h34_mac = '00:00:00:00:03:140'

h41_mac = '00:00:00:00:04:40'
h42_mac = '00:00:00:00:04:41'
h43_mac = '00:00:00:00:04:100'
h44_mac = '00:00:00:00:04:120'
h45_mac = '00:00:00:00:04:140'

all_mac = [h11_mac,h12_mac,h13_mac,h14_mac,
           h15_mac,h16_mac,h17_mac,h18_mac,
           h19_mac,h21_mac,h22_mac,h23_mac,
           h24_mac,h25_mac,h31_mac,h32_mac,
           h33_mac,h34_mac,h41_mac,h42_mac,
           h43_mac,h44_mac,h45_mac]

# broadcast ip
bc11 = '239.255.2.0'
bc12 = '239.255.2.1'
bc13 = '239.255.4.1'
bc14 = '239.255.4.2'
bc15 = '239.255.5.1'
bc16 = '239.255.6.1'
bc17 = '239.255.7.1'
bc18 = '239.255.3.0'
bc19 = '239.255.3.1'

bc21 = '239.255.8.1'
bc22 = '239.255.8.2'
bc23 = '239.255.9.1'
bc24 = '239.255.10.1'
bc25 = '239.255.11.1'

bc31 = '239.255.12.1'
bc32 = '239.255.12.2'
bc33 = '239.255.13.1'
bc34 = '239.255.14.1'

bc41 = '239.255.15.1'
bc42 = '239.255.16.2'
bc43 = '239.255.17.1'
bc44 = '239.255.18.1'
bc45 = '239.255.19.1'

# broadcast member port define


# car 1 broadcast member
bc11_mem = [{'switch':'00-00-00-00-00-01','port':[2,3,4,5,6,7,8,9,12,13,14]},
            {'switch':'00-00-00-00-00-02','port':[1,2,3,4,5]},
            {'switch':'00-00-00-00-00-03','port':[1,2,3,4]},
            {'switch':'00-00-00-00-00-04','port':[1,2,3,4,5]}]

bc12_mem = [{'switch':'00-00-00-00-00-01','port':[1,3,4,5,6,7,8,9,12,13,14]},
            {'switch':'00-00-00-00-00-02','port':[1,2,3,4,5]},
            {'switch':'00-00-00-00-00-03','port':[1,2,3,4]},
            {'switch':'00-00-00-00-00-04','port':[1,2,3,4,5]}]

bc13_mem = [{'switch':'00-00-00-00-00-01','port':[1,2,4,7]}]

bc14_mem = [{'switch':'00-00-00-00-00-01','port':[1,2,3,7]}]

bc15_mem = [{'switch':'00-00-00-00-00-01','port':[1,2,7,12,13,14]},
            {'switch':'00-00-00-00-00-02','port':[3,4]},
            {'switch':'00-00-00-00-00-03','port':[3]},
            {'switch':'00-00-00-00-00-04','port':[3,4]}]

bc16_mem = [{'switch':'00-00-00-00-00-01','port':[1,2,7]}]

bc17_mem = [{'switch':'00-00-00-00-00-01','port':[1,2]}]

bc18_mem = [{'switch':'00-00-00-00-00-01','port':[1,2,7,9]}]

bc19_mem = [{'switch':'00-00-00-00-00-01','port':[1,2,7,8]}]

# car 2 broadcast member
bc21_mem = [{'switch':'00-00-00-00-00-01','port':[1,2,7]},
            {'switch':'00-00-00-00-00-02','port':[2,11]}]

bc22_mem = [{'switch':'00-00-00-00-00-01','port':[1,2,7]},
            {'switch':'00-00-00-00-00-02','port':[1,11]}]

bc23_mem = [{'switch':'00-00-00-00-00-01','port':[1,2,5,7]},
            {'switch':'00-00-00-00-00-02','port':[4,11,13,14]},
            {'switch':'00-00-00-00-00-03','port':[3]},
            {'switch':'00-00-00-00-00-04','port':[3,4]}]

bc24_mem = [{'switch':'00-00-00-00-00-01','port':[1,2,5,7]},
            {'switch':'00-00-00-00-00-02','port':[3,11,13,14]},
            {'switch':'00-00-00-00-00-03','port':[3]},
            {'switch':'00-00-00-00-00-04','port':[3,4]}]

bc25_mem = [{'switch':'00-00-00-00-00-01','port':[1,2,7]},
            {'switch':'00-00-00-00-00-02','port':[11]}]

# car 3 broadcast member
bc31_mem = [{'switch':'00-00-00-00-00-01','port':[1,2,7]},
            {'switch':'00-00-00-00-00-03','port':[2,11]}]

bc32_mem = [{'switch':'00-00-00-00-00-01','port':[1,2,7]},
            {'switch':'00-00-00-00-00-03','port':[1,11]}]

bc33_mem = [{'switch':'00-00-00-00-00-01','port':[1,2,5,7]},
            {'switch':'00-00-00-00-00-02','port':[3,4]},
            {'switch':'00-00-00-00-00-03','port':[11,12,14]},
            {'switch':'00-00-00-00-00-04','port':[3,4]}]

bc34_mem = [{'switch':'00-00-00-00-00-01','port':[1,2,7]},
            {'switch':'00-00-00-00-00-03','port':[11]}]

# car 4 broadcast member
bc41_mem = [{'switch':'00-00-00-00-00-01','port':[1,2,7]},
            {'switch':'00-00-00-00-00-04','port':[2,11]}]

bc42_mem = [{'switch':'00-00-00-00-00-01','port':[1,2,7]},
            {'switch':'00-00-00-00-00-04','port':[1,11]}]

bc43_mem = [{'switch':'00-00-00-00-00-01','port':[1,2,5,7]},
            {'switch':'00-00-00-00-00-02','port':[3,4]},
            {'switch':'00-00-00-00-00-03','port':[3]},
            {'switch':'00-00-00-00-00-04','port':[4,11,12,13]}]

bc44_mem = [{'switch':'00-00-00-00-00-01','port':[1,2,5,7]},
            {'switch':'00-00-00-00-00-02','port':[3,4]},
            {'switch':'00-00-00-00-00-03','port':[3]},
            {'switch':'00-00-00-00-00-04','port':[3,11,12,13]}]

bc45_mem = [{'switch':'00-00-00-00-00-01','port':[1,2,7]},
            {'switch':'00-00-00-00-00-04','port':[11]}]


broad_cast_mem = [  {'broadcast_ip':bc11,'member':bc11_mem},
                    {'broadcast_ip':bc12,'member':bc12_mem},
                    {'broadcast_ip':bc13,'member':bc13_mem},
                    {'broadcast_ip':bc14,'member':bc14_mem},
                    {'broadcast_ip':bc15,'member':bc15_mem},
                    {'broadcast_ip':bc16,'member':bc16_mem},
                    {'broadcast_ip':bc17,'member':bc17_mem},
                    {'broadcast_ip':bc18,'member':bc18_mem},
                    {'broadcast_ip':bc19,'member':bc19_mem},
                    
                    {'broadcast_ip':bc21,'member':bc21_mem},
                    {'broadcast_ip':bc22,'member':bc22_mem},
                    {'broadcast_ip':bc23,'member':bc23_mem},
                    {'broadcast_ip':bc24,'member':bc24_mem},
                    {'broadcast_ip':bc25,'member':bc25_mem},
                    
                    {'broadcast_ip':bc31,'member':bc31_mem},
                    {'broadcast_ip':bc32,'member':bc32_mem},
                    {'broadcast_ip':bc33,'member':bc33_mem},
                    {'broadcast_ip':bc34,'member':bc34_mem},
                    
                    {'broadcast_ip':bc41,'member':bc41_mem},
                    {'broadcast_ip':bc42,'member':bc42_mem},
                    {'broadcast_ip':bc43,'member':bc43_mem},
                    {'broadcast_ip':bc44,'member':bc44_mem},
                    {'broadcast_ip':bc45,'member':bc45_mem}
                    ]



log = core.getLogger()

table={}


rules=[ {'src_ip' : h11_ip, 'dst_ip' : bc11},
        {'src_ip' : h12_ip, 'dst_ip' : bc12},
        {'src_ip' : h13_ip, 'dst_ip' : bc13},
        {'src_ip' : h14_ip, 'dst_ip' : bc14},
        {'src_ip' : h15_ip, 'dst_ip' : bc15},
        {'src_ip' : h16_ip, 'dst_ip' : bc16},
        {'src_ip' : h17_ip, 'dst_ip' : bc17},
        {'src_ip' : h18_ip, 'dst_ip' : bc18},
        {'src_ip' : h19_ip, 'dst_ip' : bc19},
        
        {'src_ip' : h21_ip, 'dst_ip' : bc21},
        {'src_ip' : h22_ip, 'dst_ip' : bc22},
        {'src_ip' : h23_ip, 'dst_ip' : bc23},
        {'src_ip' : h24_ip, 'dst_ip' : bc24},
        {'src_ip' : h25_ip, 'dst_ip' : bc25},
        
        {'src_ip' : h31_ip, 'dst_ip' : bc31},
        {'src_ip' : h32_ip, 'dst_ip' : bc32},
        {'src_ip' : h33_ip, 'dst_ip' : bc33},
        {'src_ip' : h34_ip, 'dst_ip' : bc34},
        
        {'src_ip' : h41_ip, 'dst_ip' : bc41},
        {'src_ip' : h42_ip, 'dst_ip' : bc42},
        {'src_ip' : h43_ip, 'dst_ip' : bc43},
        {'src_ip' : h44_ip, 'dst_ip' : bc44},
        {'src_ip' : h45_ip, 'dst_ip' : bc45}
         ]
def launch ():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn",  _handle_PacketIn)
    log.info("Switch running.")

def _handle_ConnectionUp ( event):
    log.info("Starting Switch %s", dpidToStr(event.dpid))
    msg = of.ofp_flow_mod(command = of.OFPFC_DELETE)
    event.connection.send(msg)


def _handle_PacketIn ( event): # Ths is the main class where your code goes, it will be called every time a packet is sent from the switch to the controller

    dpid = event.connection.dpid
    sw=dpidToStr(event.dpid)
    inport = event.port     
    eth_packet = event.parsed 
    log.debug("Event: switch %s port %s packet %s" % (sw, inport, eth_packet))
    # convert all_mac to EthAddr
    all_mac_eth_type =  [EthAddr(mac) for mac in all_mac]


    table[(event.connection,eth_packet.src)] = event.port   # this associates the given port with the sending node using the source address of the incoming packet
    dst_port = table.get((event.connection,eth_packet.dst)) # if available in the table this line determines the destination port of the incoming packet

    # broadcast the ARP message
    if dst_port is None and eth_packet.type == eth.ARP_TYPE and eth_packet.dst == EthAddr(b"\xff\xff\xff\xff\xff\xff"):
        msg = of.ofp_packet_out(data=event.ofp)
        msg.actions.append(of.ofp_action_output(port=of.OFPP_ALL))
        event.connection.send(msg)
    else:
        # check if eth_packet.dst is in all_mac or eth_packet.src is in all_mac
        # transfer all_mac elements to EthAddr

        if (eth_packet.dst in all_mac_eth_type or eth_packet.src in all_mac_eth_type) and dst_port is not None:
            log.debug("Event: found rule from source %s to dest  %s" % (eth_packet.src, eth_packet.dst))
            flow_mod = of.ofp_flow_mod()
            flow_mod.match.dl_src = eth_packet.src
            flow_mod.match.dl_dst = eth_packet.dst
            flow_mod.actions.append(of.ofp_action_output(port=dst_port))
            event.connection.send(flow_mod)
            
            msg = of.ofp_packet_out()
            msg.data = event.ofp
            msg.actions.append(of.ofp_action_output(port=dst_port))
        
        # for rule in rules:
        #     if eth_packet.type == eth.IP_TYPE:
        #         if eth_packet.payload.protocol == ip.UDP_PROTOCOL:
        #             if eth_packet.payload.payload.dstip == rule['dst_ip'] and eth_packet.payload.srcip == rule['src_ip']:
        #                 # create a flow mod message
        #                 msg = of.ofp_flow_mod()
        #                 # set the match
        #                 msg.match.dl_type = eth_packet.type
        #                 msg.match.nw_proto = eth_packet.payload.protocol
        #                 msg.match.nw_src = eth_packet.payload.srcip
        #                 msg.match.nw_dst = eth_packet.payload.payload.dstip
        #                 # set the action
        #                 # check broad_cast_mem for the member
        #                 for broad in broad_cast_mem:
        #                     if broad['broadcast_ip'] == rule['dst_ip']:
        #                         for mem in broad['member']:
        #                             if mem['switch'] == sw:
        #                                 for port in mem['port']:
        #                                     msg.actions.append(of.ofp_action_output(port=port))
        #                 # set available time
        #                 msg.idle_timeout = 10
        #                 msg.hard_timeout = 30
        #                 # send the message
        #                 event.connection.send(msg)
        #                 break
        # build rules for basic comm
        # flow_mod = of.ofp_flow_mod()
        # flow_mod.match.dl_src = eth_packet.src
        # flow_mod.match.dl_dst = eth_packet.dst
        # flow_mod.actions.append(of.ofp_action_output(port=dst_port))
        # flow_mod.hard_timeout = 50
        # event.connection.send(flow_mod)
        # # also send the packet
        # msg = of.ofp_packet_out()
        # msg.data = event.ofp
        # msg.actions.append(of.ofp_action_output(port=dst_port))
        # event.connection.send(msg)
                
            
            





