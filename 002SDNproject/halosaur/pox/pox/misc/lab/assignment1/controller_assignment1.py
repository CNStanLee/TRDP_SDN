'''
Author: Changhongli lic9@tcd.com
Date: 2024-03-27 16:31:08
LastEditors: Changhongli lic9@tcd.com
LastEditTime: 2024-04-08 13:11:12
FilePath: /MininetLab/pox/pox/misc/lab/assignment1/controller_assignment1.py
Description: 

'''
# ------------------------------------------------------------------------------------------- #
# import libs
# ------------------------------------------------------------------------------------------- #
from pox.core import core
import pox.lib.packet as pkt
import pox.lib.packet.ethernet as eth
import pox.lib.packet.arp as arp
import pox.lib.packet.icmp as icmp
import pox.lib.packet.ipv4 as ip
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
# ------------------------------------------------------------------------------------------- #
# Variables def
# ------------------------------------------------------------------------------------------- #
log = core.getLogger()
table={}
rule_cap50 = 0;
rule_cap100 = 1;
rule_cap500 = 2;
rule_capfree = 3;
rule_block = 4;
rule_cap250 = 5;

h1_mac = '00:00:00:00:00:02'
h2_mac = '00:00:00:00:00:03'
h3_mac = '00:00:00:00:00:04'
h4_mac = '00:00:00:00:00:05'

# rules like src -> dst

# rule matrix
#       h1  h2  h3  h4
#   h1  /   x   50  250
#   h2  x   /   100 500
#   h3  250   o   /   ok
#   h4  250   o   o   /

# h1 should be limited as 250
# rules should be expired after 40s


rules=[
    #{'EthSrc':h1_mac,'EthDst':h2_mac, 'queue':rule_block},
    {'EthSrc':h1_mac,'EthDst':h3_mac, 'queue':rule_cap50},
    {'EthSrc':h1_mac,'EthDst':h4_mac, 'queue':rule_cap250},
 
    #{'EthSrc':h2_mac,'EthDst':h1_mac, 'queue':rule_block},
    {'EthSrc':h2_mac,'EthDst':h3_mac, 'queue':rule_cap100},
    {'EthSrc':h2_mac,'EthDst':h4_mac, 'queue':rule_cap500},

    {'EthSrc':h3_mac,'EthDst':h1_mac, 'queue':rule_cap250},
    {'EthSrc':h3_mac,'EthDst':h2_mac, 'queue':rule_capfree},
    {'EthSrc':h3_mac,'EthDst':h4_mac, 'queue':rule_capfree},
    
    {'EthSrc':h4_mac,'EthDst':h1_mac, 'queue':rule_cap250},
    {'EthSrc':h4_mac,'EthDst':h2_mac, 'queue':rule_capfree},
    {'EthSrc':h4_mac,'EthDst':h3_mac, 'queue':rule_capfree}
    	# => the first two example of rules have been added for you, you need now to add other rules to satisfy the assignment requirements. Notice that we will make decisions based on Ethernet address rather than IP address. Rate limiting is implemented by sending the pacet to the correct port and queue (the queues that you have specified in the topology file).
      ]



# ------------------------------------------------------------------------------------------- #
# Functions def
# ------------------------------------------------------------------------------------------- #
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
    inport = event.port     # this records the port from which the packet entered the switch
    eth_packet = event.parsed # this parses  the incoming message as an Ethernet packet
    log.debug("Event: switch %s port %s packet %s" % (sw, inport, eth_packet)) # this is the way you can add debugging information to your text

    table[(event.connection,eth_packet.src)] = event.port   # this associates the given port with the sending node using the source address of the incoming packet
    dst_port = table.get((event.connection,eth_packet.dst)) # if available in the table this line determines the destination port of the incoming packet


    if dst_port is None and eth_packet.type == eth.ARP_TYPE and eth_packet.dst == EthAddr(b"\xff\xff\xff\xff\xff\xff"):  # this identifies that the packet is an ARP broadcast
    	# => in this case you want to create a packet so that you can send the message as a broadcast
        msg = of.ofp_packet_out(data = event.ofp)
        msg.actions.append(of.ofp_action_output(port = of.OFPP_ALL))
        event.connection.send(msg)
    else:
        for rule in rules: # now you want to start adding your rules in the flow table. Every time you go through the rules table to check if there is a rule to handle this source-to-destination flow
            if eth_packet.src==EthAddr(rule['EthSrc']) and eth_packet.dst==EthAddr(rule['EthDst']):
                # set rules
                msg = of.ofp_flow_mod()
                msg.match.dl_src = eth_packet.src
                msg.match.dl_dst = eth_packet.dst
                #msg.actions = [of.ofp_action_output(port=dst_port)]
                msg.actions = [of.ofp_action_enqueue(port=dst_port, queue_id=rule['queue'])]
                msg.hard_timeout = 40
                # Send the flow mod message to the switch to add the new rule
                event.connection.send(msg)
                
                # send msg    
                msg = of.ofp_packet_out()
                msg.data = event.ofp
                msg.actions.append(of.ofp_action_output(port = dst_port))
                event.connection.send(msg)
                break
