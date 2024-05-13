'''
Author: Changhongli lic9@tcd.com
Date: 2024-04-08 18:13:46
LastEditors: Changhongli lic9@tcd.com
LastEditTime: 2024-04-09 21:12:42
FilePath: /MininetLab/pox/pox/misc/lab/assignment2/controller_assignment2.py
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


log = core.getLogger()

table={}

cap_50 = 0
cap_100 = 1
cap_500 = 2

rules=[{'EthSrc':'00:00:00:00:00:01', 'EthDst':'00:00:00:00:00:03', 'TCPPort':30, 'queue':cap_50},
         {'EthSrc':'00:00:00:00:00:02', 'EthDst':'00:00:00:00:00:03', 'TCPPort':50, 'queue':cap_100},
         {'EthSrc':'00:00:00:00:00:03', 'EthDst':'00:00:00:00:00:02', 'TCPPort':None, 'queue':None},
         {'EthSrc':'00:00:00:00:00:03', 'EthDst':'00:00:00:00:00:01', 'TCPPort':None, 'queue':None},
         
         {'EthSrc':'00:00:00:00:00:01', 'EthDst':'00:00:00:00:00:04', 'TCPPort':80, 'queue':None},
         {'EthSrc':'00:00:00:00:00:02', 'EthDst':'00:00:00:00:00:04', 'TCPPort':80, 'queue':None},
         {'EthSrc':'00:00:00:00:00:03', 'EthDst':'00:00:00:00:00:04', 'TCPPort':90, 'queue':cap_500},
         
         {'EthSrc':'00:00:00:00:00:04', 'EthDst':'00:00:00:00:00:03', 'TCPPort':None, 'queue':None},
         {'EthSrc':'00:00:00:00:00:04', 'EthDst':'00:00:00:00:00:02', 'TCPPort':None, 'queue':None},
         {'EthSrc':'00:00:00:00:00:04', 'EthDst':'00:00:00:00:00:01', 'TCPPort':None, 'queue':None},
         
         {'EthSrc':'00:00:00:00:00:01', 'EthDst':'00:00:00:00:00:02', 'TCPPort':None, 'queue':None},
         {'EthSrc':'00:00:00:00:00:02', 'EthDst':'00:00:00:00:00:01', 'TCPPort':None, 'queue':None}
         ]
    # => This is similar to the previous assignment, but notice that now you also have to define the TPC field.
    
def launch ():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn",  _handle_PacketIn)
    log.info("Switch running.v2")

def _handle_ConnectionUp ( event):
    log.info("Starting Switch %s", dpidToStr(event.dpid))
    msg = of.ofp_flow_mod(command = of.OFPFC_DELETE)
    event.connection.send(msg)


def _handle_PacketIn ( event): # Ths is the main class where your code goes, it will be called every time a packet is sent from the switch to the controller

    dpid = event.connection.dpid
    sw=dpidToStr(event.dpid)
    inport = event.port     # this records the port from which the packet entered the switch
    eth_packet = event.parsed # this parses  the incoming message as an Ethernet packet
    log.debug("Event: switch %s port %s packet %s" % (sw, inport, eth_packet)) # this is the way you can add debugging information to your text

    table[(event.connection,eth_packet.src)] = event.port   # this associates the given port with the sending node using the source address of the incoming packet
    dst_port = table.get((event.connection,eth_packet.dst)) # if available in the table this line determines the destination port of the incoming packet

# this part is now separate from next part and deals with ARP messages 

    if dst_port is None and eth_packet.type == eth.ARP_TYPE and eth_packet.dst == EthAddr(b"\xff\xff\xff\xff\xff\xff"):
        # => this is the same as for the first assignment
        log.debug("Event: ARP broadcast from source %s to dest  %s" % (eth_packet.src, eth_packet.dst))
        msg = of.ofp_packet_out(data = event.ofp)
        msg.actions.append(of.ofp_action_output(port = of.OFPP_ALL))
        event.connection.send(msg)

    for rule in rules: #now you are adding rules to the flow tables like before. First you check whether there is a rule match based on Eth source and destination
        if eth_packet.src==EthAddr(rule['EthSrc']) and eth_packet.dst==EthAddr(rule['EthDst']):
            log.debug("Event: found rule from src %s to dst  %s" % (eth_packet.src, eth_packet.dst))
            # => start creating a new flow rule for mathcing the ethernet source and destination
            flow_mod = of.ofp_flow_mod()
            flow_mod.match.dl_src = eth_packet.src
            flow_mod.match.dl_dst = eth_packet.dst
            # => now check if the rule contains also TCP port info. If not install the flow without any port restriction
            if rule['TCPPort'] is None:
                log.debug("don't need to check TCP port")
            # => otherwise:tcp_src': 80, 'qu
                if eth_packet.type == eth.ARP_TYPE:
                    msg = of.ofp_packet_out(data = event.ofp)
                    msg.actions.append(of.ofp_action_output(port = of.OFPP_ALL))
                    event.connection.send(msg)
               
                # => if the packet is an IP packet, its protocol is TCP, and the TCP port of teh packet matches the TCP rule above
                elif eth_packet.type == eth.IP_TYPE and eth_packet.payload.protocol == pkt.ipv4.TCP_PROTOCOL:# and eth_packet.payload.payload.dstport == rule['TCPPort']:
                    # => add additioinal matching fileds to the flow rule you are creating: IP-protocol type, TCP_protocol_type, destination TCP port.
                    if eth_packet.payload.payload.dstport == rule['TCPPort']:
                        flow_mod.match.dl_type = pkt.ethernet.IP_TYPE
                        flow_mod.match.nw_proto = pkt.ipv4.TCP_PROTOCOL
                        flow_mod.match.tp_dst = eth_packet.payload.payload.dstport
                    else:
                        flow_mod.match.dl_type = pkt.ethernet.IP_TYPE
                        flow_mod.match.nw_proto = pkt.ipv4.TCP_PROTOCOL
                        flow_mod.match.tp_dst = eth_packet.payload.payload.dstport
                        flow_mod.actions.append(of.ofp_action_output(port=of.OFPP_NONE))
                        flow_mod.hard_timeout = 50
                        event.connection.send(flow_mod)
                        break
            if rule['queue'] is not None:
                flow_mod.actions.append(of.ofp_action_enqueue(port=dst_port, queue_id=rule['queue']))
            else:
                flow_mod.actions.append(of.ofp_action_output(port=dst_port))
            # => send the flow_mod to the switch
            flow_mod.hard_timeout = 50
            event.connection.send(flow_mod)
	        # => then remember to still send out this packet
            msg = of.ofp_packet_out()
            msg.data = event.ofp
            msg.actions.append(of.ofp_action_output(port = dst_port))
            event.connection.send(msg)
	        # YOUR CODE ENDS HERE
            break

