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

rules = [
    {'EthSrc':'00:00:00:00:00:01', 'EthDst':'00:00:00:00:00:03', 'tcp_src': 30, 'queue':1}, # cap 50
    {'EthSrc':'00:00:00:00:00:03', 'EthDst':'00:00:00:00:00:01', 'tcp_src': None, 'queue':0}, # not capped
    {'EthSrc':'00:00:00:00:00:01', 'EthDst':'00:00:00:00:00:04', 'tcp_src': 80, 'queue':0}, # not capped
    
    {'EthSrc':'00:00:00:00:00:02', 'EthDst':'00:00:00:00:00:03', 'tcp_src': 50, 'queue':2}, # cap 100
    {'EthSrc':'00:00:00:00:00:03', 'EthDst':'00:00:00:00:00:02', 'tcp_src': None, 'queue':0}, # not capped

    {'EthSrc':'00:00:00:00:00:02', 'EthDst':'00:00:00:00:00:04', 'tcp_src': 80, 'queue':0}, # not capped

    {'EthSrc':'00:00:00:00:00:03', 'EthDst':'00:00:00:00:00:04', 'tcp_src': 90, 'queue':3},# cap 500

    {'EthSrc':'00:00:00:00:00:04', 'EthDst':'00:00:00:00:00:01', 'tcp_src': None, 'queue':0},
    {'EthSrc':'00:00:00:00:00:04', 'EthDst':'00:00:00:00:00:02', 'tcp_src': None, 'queue':0},
    {'EthSrc':'00:00:00:00:00:04', 'EthDst':'00:00:00:00:00:03', 'tcp_src': None, 'queue':0},

    # {'EthSrc':'00:00:00:00:00:01', 'EthDst':'00:00:00:00:00:02', 'TcpPort': 80, 'queue':0}, # not capped
    # {'EthSrc':'00:00:00:00:00:02', 'EthDst':'00:00:00:00:00:01', 'TcpPort': 80, 'queue':0}, # not capped
]

def launch ():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn",  _handle_PacketIn)
    log.info("Switch running.")

def _handle_ConnectionUp ( event):
    log.info("Starting Switch %s", dpidToStr(event.dpid))
    msg = of.ofp_flow_mod(command = of.OFPFC_DELETE)
    event.connection.send(msg)

def _handle_PacketIn(event): # Ths is the main class where your code goes, it will be called every time a packet is sent from the switch to the controller
    dpid = event.connection.dpid
    sw=dpidToStr(event.dpid)
    inport = event.port     # this records the port from which the packet entered the switch
    eth_packet = event.parsed # this parses  the incoming message as an Ethernet packet

    table[(event.connection,eth_packet.src)] = event.port   # this associates the given port with the sending node using the source address of the incoming packet
    dst_port = table.get((event.connection,eth_packet.dst)) # if available in the table this line determines the destination port of the incoming packet

    if dst_port is None and eth_packet.type == eth.ARP_TYPE and eth_packet.dst == EthAddr(b"\xff\xff\xff\xff\xff\xff"):
    	# => in this case you want to create a packet so that you can send the message as a broadcast
        action = of.ofp_action_output(port=of.OFPP_ALL)
        msg = of.ofp_packet_out(data=event.data, actions=[action], in_port=inport)
        event.connection.send(msg)

    
    else:
        for rule in rules:  # Start adding your rules in the flow table.
            if eth_packet.src == EthAddr(rule['EthSrc']) and eth_packet.dst == EthAddr(rule['EthDst']):
                action = [of.ofp_action_output(port=dst_port)]
                msg = of.ofp_flow_mod(command=of.OFPFC_ADD)
                # =>create a new flow rule and install it in the switch.
                # and remember to also use the queue information if this is present in the rules list.
                print('eth_packet ', eth_packet)
                # Create and send flow mod message to install the rule
                

                if rule['tcp_src'] is not None:

                    #if eth_packet.type == eth.IP_TYPE and eth_packet.find('ipv4').protocol == ip.TCP_PROTOCOL:
                    if eth_packet.type == eth.ARP_TYPE:
                        action = of.ofp_action_output(port=of.OFPP_ALL)
                        msg.match = of.ofp_match(dl_type = eth.ARP_TYPE, dl_src = EthAddr(rule['EthSrc']), dl_dst = EthAddr(rule['EthDst']))
                        print('match ARP')
                    elif eth_packet.type == eth.IP_TYPE:
                        ip_pkg = eth_packet.payload
                        if eth_packet.find('ipv4').protocol == ip.TCP_PROTOCOL:
                            if eth_packet.payload.payload.dstport == rule['tcp_src']:
                                msg.match = of.ofp_match(dl_type = eth_packet.type, nw_proto = ip_pkg.protocol, tp_dst = eth_packet.payload.payload.dstport, \
                                                        dl_src = EthAddr(rule['EthSrc']), dl_dst = EthAddr(rule['EthDst']), \
                                                        nw_src = ip_pkg.srcip, nw_dst = ip_pkg.dstip)
                                print('match IP TCP Ture port')
                            else:
                                break
                        else:
                            break
                    else:
                        break
                else:
                    msg.match = of.ofp_match(dl_src = EthAddr(rule['EthSrc']), dl_dst = EthAddr(rule['EthDst']))
                
                if 'queue' in rule and rule['queue'] is not None:
                    action = [of.ofp_action_enqueue(port=dst_port, queue_id=rule['queue'])]
                msg.actions = action
                msg.hard_timeout = 50
                event.connection.send(msg)

               # =>after this you will need to also send the message you have received back to the switch, after setting the correct destination port
                data_packet_out = of.ofp_packet_out(buffer_id=event.ofp.buffer_id,in_port=dst_port, actions=action)
                event.connection.send(data_packet_out)

               # YOUR CODE ENDS HERE
                break 
