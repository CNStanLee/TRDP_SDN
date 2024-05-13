'''
Author: Changhongli lic9@tcd.com
Date: 2024-03-21 12:00:37
LastEditors: Changhongli lic9@tcd.com
LastEditTime: 2024-03-27 22:12:15
FilePath: /pox/pox/misc/lab/lab2/simple_controller.py
Description: 

'''
# ------------------------------------------------------------------------------------------- #
# import libs
# ------------------------------------------------------------------------------------------- #
from pox.core import core                       # POX core functions
import pox.lib.packet as pkt                    # Network packet
import pox.openflow.libopenflow_01 as of        # Openflow
from pox.lib.util import dpidToStr              # transfer swith's ID(DPID) to string
from pox.lib.addresses import EthAddr           # deal with eth addr format
# ------------------------------------------------------------------------------------------- #
# Variables def
# ------------------------------------------------------------------------------------------- #
# rules : src -> dst  => [[src, dst]]
# log   : pox log
# table : to storage mapping realationships
rules=[['00:00:00:00:00:01','00:00:00:00:00:02'],['00:00:00:00:00:03', '00:00:00:00:00:04']]
log = core.getLogger()
table={}
# ------------------------------------------------------------------------------------------- #
# Functions def
# ------------------------------------------------------------------------------------------- #
# launch : start the SDN switch, add listener for connecitonup and packetin
# _handle_ConnectionUp: event when connection up
def launch ():
    # regist event listener, when connection up => _handle_ConnectionUp
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    # regist event listener
    core.openflow.addListenerByName("PacketIn",  _handle_PacketIn)
    log.info("Switch running.")
# ------------------------------------------------------------------------------------------- #
# Firewall Application
# ------------------------------------------------------------------------------------------- #
def _handle_ConnectionUp ( event):
    # switch begins to work
    log.info("Starting Switch %s", dpidToStr(event.dpid))
    # Create an openflow msg to del all the Flow Entry
    # Flow Entry is a group of rules which contain Match Fields and Instructions
    msg = of.ofp_flow_mod(command = of.OFPFC_DELETE)
    # Connect and send messages
    event.connection.send(msg)
    for rule in rules:
        # Create openflow match obj
        block = of.ofp_match()
        # SRC MAC add -> rule(0)
        block.dl_src = EthAddr(rule[0])
        # DST MAC add -> rule(1)
        block.dl_dst = EthAddr(rule[1])
        # Create flow entry
        flow_mod = of.ofp_flow_mod()
        # Set rules
        flow_mod.match = block
        flow_mod.priority = 32000
        event.connection.send(flow_mod)
# ------------------------------------------------------------------------------------------- #
# Forward Application
# ------------------------------------------------------------------------------------------- #
def _handle_PacketIn ( event):
    # get the id of the switch
    dpid = event.connection.dpid
    sw=dpidToStr(event.dpid)
    # data input port
    inport = event.port
    # data pack
    packet = event.parsed
    print("Event: switch %s port %s packet %s" % (sw, inport, packet))
    # Learn the source and save to the table
    table[(event.connection,packet.src)] = event.port
    # dst port of the pack
    dst_port = table.get((event.connection,packet.dst))

    if dst_port is None:
        #  The switch does not know the destination, so sends the message out all ports.(broadcast)
        #  We could use either of the special ports OFPP_FLOOD or OFP_ALL.
        #  But not all switches support OFPP_FLOOD. 
        msg = of.ofp_packet_out(data = event.ofp)
        msg.actions.append(of.ofp_action_output(port = of.OFPP_ALL))
        event.connection.send(msg)
    else:
        # The switch knows the destination, so can route the packet. We also install the forward rule into the switch
        # forward rules
        msg = of.ofp_flow_mod()
        msg.priority=100
        msg.match.dl_dst = packet.src
        msg.match.dl_src = packet.dst
        msg.actions.append(of.ofp_action_output(port = event.port))
        event.connection.send(msg)

        # We must forward the incoming packet…
        # forward data
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port = dst_port))
        event.connection.send(msg)

        log.debug("Installing %s <-> %s" % (packet.src, packet.dst))