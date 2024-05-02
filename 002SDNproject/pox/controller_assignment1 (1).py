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

rules=[{'EthSrc':'00:00:00:00:00:01','EthDst':'00:00:00:00:00:03', 'queue':0},
    {'EthSrc':'00:00:00:00:00:03','EthDst':'00:00:00:00:00:01', 'queue':None},
    	# => the first two example of rules have been added for you, you need now to add other rules to satisfy the assignment requirements. Notice that we will make decisions based on Ethernet address rather than IP address. Rate limiting is implemented by sending the pacet to the correct port and queue (the queues that you have specified in the topology file).
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
    inport = event.port     # this records the port from which the packet entered the switch
    eth_packet = event.parsed # this parses  the incoming message as an Ethernet packet
    log.debug("Event: switch %s port %s packet %s" % (sw, inport, eth_packet)) # this is the way you can add debugging information to your text

    table[(event.connection,eth_packet.src)] = event.port   # this associates the given port with the sending node using the source address of the incoming packet
    dst_port = table.get((event.connection,eth_packet.dst)) # if available in the table this line determines the destination port of the incoming packet


    if dst_port is None and eth_packet.type == eth.ARP_TYPE and eth_packet.dst == EthAddr(b"\xff\xff\xff\xff\xff\xff"):  # this identifies that the packet is an ARP broadcast
    	# => in this case you want to create a packet so that you can send the message as a broadcast

    for rule in rules: # now you want to start adding your rules in the flow table. Every time you go through the rules table to check if there is a rule to handle this source-to-destination flow
        if eth_packet.src==EthAddr(rule['EthSrc']) and eth_packet.dst==EthAddr(rule['EthDst']):
            # =>create a new flow rule and install it in the switch
            # and remember to also use the queue information if this is present in the rules list

	    # =>after this you will need to also send the message you have received back to the switch, after setting the correct destination port


	 # YOUR CODE ENDS HERE
            break

