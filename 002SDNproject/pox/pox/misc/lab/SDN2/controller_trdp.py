'''
Author: Changhongli lic9@tcd.com
Date: 2024-04-09 22:12:43
LastEditors: Changhongli lic9@tcd.com
LastEditTime: 2024-04-28 22:01:03
FilePath: /pox/pox/misc/lab/SDN2/controller_trdp.py
Description: 

'''
from pox.core import core
import time
import pox.lib.packet as pkt
import pox.lib.packet.ethernet as eth
import pox.lib.packet.arp as arp
import pox.lib.packet.icmp as icmp
import pox.lib.packet.ipv4 as ip
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr, IPAddr


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
h16_mac = '00:00:00:00:01:8c'
h17_mac = '00:00:00:00:01:d2'
h18_mac = '00:00:00:00:01:30'
h19_mac = '00:00:00:00:01:31'

h21_mac = '00:00:00:00:02:40'
h22_mac = '00:00:00:00:02:41'
h23_mac = '00:00:00:00:02:64'
h24_mac = '00:00:00:00:02:78'
h25_mac = '00:00:00:00:02:8c'

h31_mac = '00:00:00:00:03:40'
h32_mac = '00:00:00:00:03:41'
h33_mac = '00:00:00:00:03:78'
h34_mac = '00:00:00:00:03:8c'

h41_mac = '00:00:00:00:04:40'
h42_mac = '00:00:00:00:04:41'
h43_mac = '00:00:00:00:04:64'
h44_mac = '00:00:00:00:04:78'
h45_mac = '00:00:00:00:04:8c'

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
SW1 = '00-00-00-00-00-01'
SW2 = '00-00-00-00-00-02'
SW3 = '00-00-00-00-00-03'
SW4 = '00-00-00-00-00-04'
SWITCHES = [SW1, SW2, SW3, SW4]

TRUNK_PORTS = {
    SW1: [12, 13, 14],
    SW2: [11, 13, 14],
    SW3: [11, 12, 14],
    SW4: [11, 12, 13],
}

TRDP_VLAN = 100
TRDP_VLAN_PCP = 5
LOW_PRIORITY_QUEUE = 1

COOKIE = {
    'base': 0xb000001,
    'd1': 0xd100001,
    'd2': 0xd200001,
    'd3': 0xd300001,
    'd4': 0xd400001,
    'd5': 0xd500001,
}

STRATEGIES = [
    {'id': 'd1', 'description': 'Creating an ACL', 'cost': 1.5},
    {'id': 'd2', 'description': 'Deploying VLAN Trunks for TRDP Communications', 'cost': 3.3},
    {'id': 'd3', 'description': 'Adjusting QoS to downgrade priority of malicious packets', 'cost': 4.6},
    {'id': 'd4', 'description': 'Restricting traffic on ports of abnormal hosts', 'cost': 1.8},
    {'id': 'd5', 'description': 'Isolating ports and preventing data transmission', 'cost': 8.6},
]

ACL_RULES = [
    {'switch': SW1, 'port': 7, 'src_ip': h17_ip, 'dst_ip': bc17},
    {'switch': SW2, 'port': 5, 'src_ip': h25_ip, 'dst_ip': bc25},
    {'switch': SW3, 'port': 4, 'src_ip': h34_ip, 'dst_ip': bc34},
    {'switch': SW4, 'port': 5, 'src_ip': h45_ip, 'dst_ip': bc45},
]

QOS_RULES = [
    {'switch': SW1, 'port': 6, 'src_ip': h16_ip, 'dst_ip': bc16},
    {'switch': SW2, 'port': 5, 'src_ip': h25_ip, 'dst_ip': bc25},
    {'switch': SW3, 'port': 4, 'src_ip': h34_ip, 'dst_ip': bc34},
    {'switch': SW4, 'port': 5, 'src_ip': h45_ip, 'dst_ip': bc45},
]

RESTRICTED_PORTS = [
    {'switch': SW1, 'port': 7, 'src_ip': h17_ip, 'allowed_ports': [1, 2]},
    {'switch': SW2, 'port': 5, 'src_ip': h25_ip, 'allowed_ports': [11]},
    {'switch': SW3, 'port': 4, 'src_ip': h34_ip, 'allowed_ports': [11]},
    {'switch': SW4, 'port': 5, 'src_ip': h45_ip, 'allowed_ports': [11]},
]

ISOLATED_PORTS = [
    {'switch': SW1, 'port': 7, 'ip': h17_ip},
    {'switch': SW2, 'port': 5, 'ip': h25_ip},
    {'switch': SW3, 'port': 4, 'ip': h34_ip},
    {'switch': SW4, 'port': 5, 'ip': h45_ip},
]

_policy_deployer = None


def _as_bool(value):
    return str(value).lower() in ('1', 'true', 'yes', 'on')


def _members_for(broadcast_ip, switch):
    for broad in broad_cast_mem:
        if broad['broadcast_ip'] == broadcast_ip:
            for member in broad['member']:
                if member['switch'] == switch:
                    return list(member['port'])
    return []


def _unique_ports(ports):
    return sorted(set(ports))


def _output_actions(ports):
    return [of.ofp_action_output(port=port) for port in _unique_ports(ports)]


def _udp_match(src_ip=None, dst_ip=None, in_port=None, vlan=None):
    match = of.ofp_match()
    match.dl_type = eth.IP_TYPE
    match.nw_proto = ip.UDP_PROTOCOL
    if src_ip is not None:
        match.nw_src = IPAddr(src_ip)
    if dst_ip is not None:
        match.nw_dst = IPAddr(dst_ip)
    if in_port is not None:
        match.in_port = in_port
    if vlan is not None:
        match.dl_vlan = vlan
    return match


def _ip_dst_match(dst_ip):
    match = of.ofp_match()
    match.dl_type = eth.IP_TYPE
    match.nw_dst = IPAddr(dst_ip)
    return match


def _arp_dst_match(dst_ip):
    match = of.ofp_match()
    match.dl_type = eth.ARP_TYPE
    match.nw_dst = IPAddr(dst_ip)
    return match


def _in_port_match(in_port):
    match = of.ofp_match()
    match.in_port = in_port
    return match


def _flow_mod(priority, match, actions=None, cookie=0):
    msg = of.ofp_flow_mod()
    msg.priority = priority
    msg.cookie = cookie
    msg.match = match
    for action in actions or []:
        msg.actions.append(action)
    return msg


def _install_table_miss(connection, send_to_controller=True):
    msg = of.ofp_flow_mod()
    msg.priority = 0
    if send_to_controller:
        msg.actions.append(of.ofp_action_output(port=of.OFPP_CONTROLLER))
    connection.send(msg)


def _build_base_trdp_flows(switch):
    flows = []
    for rule in rules:
        ports = _members_for(rule['dst_ip'], switch)
        if not ports:
            continue
        match = _udp_match(src_ip=rule['src_ip'], dst_ip=rule['dst_ip'])
        flows.append((switch, _flow_mod(100, match, _output_actions(ports), COOKIE['base'])))
    return flows


def _build_acl_flows():
    flows = []
    for acl in ACL_RULES:
        match = _udp_match(
            src_ip=acl['src_ip'],
            dst_ip=acl['dst_ip'],
            in_port=acl['port'],
        )
        flows.append((acl['switch'], _flow_mod(460, match, [], COOKIE['d1'])))
    return flows


def _build_vlan_flows():
    flows = []
    for rule in rules:
        for switch in SWITCHES:
            ports = _members_for(rule['dst_ip'], switch)
            if not ports:
                continue

            trunk_ports = [p for p in ports if p in TRUNK_PORTS[switch]]
            access_ports = [p for p in ports if p not in TRUNK_PORTS[switch]]
            actions = _output_actions(access_ports)
            if trunk_ports:
                actions.append(of.ofp_action_set_vlan_vid(vlan_vid=TRDP_VLAN))
                actions.append(of.ofp_action_set_vlan_pcp(vlan_pcp=TRDP_VLAN_PCP))
                actions.extend(_output_actions(trunk_ports))

            match = _udp_match(
                src_ip=rule['src_ip'],
                dst_ip=rule['dst_ip'],
                vlan=of.OFP_VLAN_NONE,
            )
            flows.append((switch, _flow_mod(250, match, actions, COOKIE['d2'])))

            for in_port in TRUNK_PORTS[switch]:
                tagged_actions = _output_actions([p for p in trunk_ports if p != in_port])
                if access_ports:
                    tagged_actions.append(of.ofp_action_strip_vlan())
                    tagged_actions.extend(_output_actions(access_ports))
                if not tagged_actions:
                    continue
                tagged_match = _udp_match(
                    src_ip=rule['src_ip'],
                    dst_ip=rule['dst_ip'],
                    in_port=in_port,
                    vlan=TRDP_VLAN,
                )
                flows.append((switch, _flow_mod(255, tagged_match, tagged_actions, COOKIE['d2'])))
    return flows


def _build_qos_flows():
    flows = []
    for qos in QOS_RULES:
        ports = [p for p in _members_for(qos['dst_ip'], qos['switch']) if p != qos['port']]
        if not ports:
            continue
        actions = [of.ofp_action_nw_tos(nw_tos=0)]
        actions.extend([of.ofp_action_enqueue(port=p, queue_id=LOW_PRIORITY_QUEUE)
                        for p in _unique_ports(ports)])
        match = _udp_match(
            src_ip=qos['src_ip'],
            dst_ip=qos['dst_ip'],
            in_port=qos['port'],
        )
        flows.append((qos['switch'], _flow_mod(330, match, actions, COOKIE['d3'])))
    return flows


def _build_restrict_flows():
    flows = []
    for restricted in RESTRICTED_PORTS:
        match = _udp_match(src_ip=restricted['src_ip'], in_port=restricted['port'])
        actions = _output_actions(restricted['allowed_ports'])
        flows.append((restricted['switch'], _flow_mod(360, match, actions, COOKIE['d4'])))
    return flows


def _build_isolate_flows():
    flows = []
    for isolated in ISOLATED_PORTS:
        flows.append((isolated['switch'],
                      _flow_mod(520, _in_port_match(isolated['port']), [], COOKIE['d5'])))
        for switch in SWITCHES:
            flows.append((switch,
                          _flow_mod(510, _ip_dst_match(isolated['ip']), [], COOKIE['d5'])))
            flows.append((switch,
                          _flow_mod(510, _arp_dst_match(isolated['ip']), [], COOKIE['d5'])))
    return flows


def _build_policy_flows(policy_id):
    if policy_id == 'd1':
        return _build_acl_flows()
    if policy_id == 'd2':
        return _build_vlan_flows()
    if policy_id == 'd3':
        return _build_qos_flows()
    if policy_id == 'd4':
        return _build_restrict_flows()
    if policy_id == 'd5':
        return _build_isolate_flows()
    return []


class PolicyDeployer(object):
    def __init__(self, measure=True, expected_switches=4):
        self.measure = measure
        self.expected_switches = expected_switches
        self.connections = {}
        self.started = False
        self.index = 0
        self.current = None
        self.results = []

    def connection_up(self, event):
        switch = dpidToStr(event.dpid)
        if switch not in SWITCHES:
            log.warning("Ignoring unexpected switch %s", switch)
            return
        self.connections[switch] = event.connection
        log.info("Policy deployer sees %d/%d switches",
                 len(self.connections), self.expected_switches)
        if self.measure and not self.started and len(self.connections) >= self.expected_switches:
            self.started = True
            core.callDelayed(0.5, self._deploy_next)

    def _deploy_next(self):
        if self.index >= len(STRATEGIES):
            self._log_summary()
            return

        strategy = STRATEGIES[self.index]
        flows = _build_policy_flows(strategy['id'])
        targets = sorted(set([sw for sw, msg in flows if sw in self.connections]))

        start = time.perf_counter()
        sent = 0
        for switch, msg in flows:
            connection = self.connections.get(switch)
            if connection is None:
                continue
            connection.send(msg)
            sent += 1
        elapsed_ms = (time.perf_counter() - start) * 1000.0

        self.results.append({
            'id': strategy['id'],
            'description': strategy['description'],
            'cost': strategy['cost'],
            'flows': len(flows),
            'sent': sent,
            'switches': len(targets),
            'elapsed_ms': elapsed_ms,
        })
        log.info("POLICY_SEND_TIME %s cost=%.1f flow_mods=%d sent=%d switches=%d elapsed_ms=%.3f description=%s",
                 strategy['id'], strategy['cost'], len(flows), sent,
                 len(targets), elapsed_ms, strategy['description'])
        self.index += 1
        core.callDelayed(0.2, self._deploy_next)

    def _log_summary(self):
        log.info("POLICY_SEND_SUMMARY_BEGIN")
        for result in self.results:
            log.info("POLICY_SEND_SUMMARY %s cost=%.1f flow_mods=%d sent=%d switches=%d elapsed_ms=%.3f",
                     result['id'], result['cost'], result['flows'],
                     result['sent'], result['switches'], result['elapsed_ms'])
        log.info("POLICY_SEND_SUMMARY_END")


def _run_selftest():
    base_flows = []
    for switch in SWITCHES:
        base_flows.extend(_build_base_trdp_flows(switch))
    for switch, msg in base_flows:
        msg.pack()
    log.info("POLICY_SELFTEST base flow_mods=%d switches=%d",
             len(base_flows), len(SWITCHES))

    for strategy in STRATEGIES:
        flows = _build_policy_flows(strategy['id'])
        for switch, msg in flows:
            msg.pack()
        log.info("POLICY_SELFTEST %s cost=%.1f flow_mods=%d description=%s",
                 strategy['id'], strategy['cost'], len(flows), strategy['description'])


def launch (measure=True, expected_switches=4, selftest=False):
    global _policy_deployer
    if _as_bool(selftest):
        _run_selftest()
        core.callDelayed(0.1, core.quit)
        return

    _policy_deployer = PolicyDeployer(
        measure=_as_bool(measure),
        expected_switches=int(expected_switches),
    )
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    if not _policy_deployer.measure:
        core.openflow.addListenerByName("PacketIn",  _handle_PacketIn)
    log.info("TRDP OpenFlow policy controller running; measure=%s expected_switches=%d",
             _policy_deployer.measure, _policy_deployer.expected_switches)


def _handle_ConnectionUp (event):
    switch = dpidToStr(event.dpid)
    log.info("Starting Switch %s", switch)
    msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)
    event.connection.send(msg)

    _install_table_miss(event.connection, send_to_controller=not _policy_deployer.measure)
    base_flows = _build_base_trdp_flows(switch)
    for flow_switch, flow in base_flows:
        event.connection.send(flow)
    log.info("Installed %d base TRDP multicast flows on %s", len(base_flows), switch)

    if _policy_deployer is not None:
        _policy_deployer.connection_up(event)


def _handle_BarrierIn(event):
    if _policy_deployer is not None:
        _policy_deployer.barrier_in(event)


def _handle_PacketIn (event):
    inport = event.port
    eth_packet = event.parsed
    if not eth_packet.parsed:
        return

    table[(event.connection, eth_packet.src)] = inport
    dst_port = table.get((event.connection, eth_packet.dst))

    if dst_port is None:
        msg = of.ofp_packet_out(data=event.ofp)
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)
        return

    flow_mod = of.ofp_flow_mod()
    flow_mod.priority = 10
    flow_mod.match.dl_src = eth_packet.src
    flow_mod.match.dl_dst = eth_packet.dst
    flow_mod.idle_timeout = 20
    flow_mod.actions.append(of.ofp_action_output(port=dst_port))
    event.connection.send(flow_mod)

    msg = of.ofp_packet_out(data=event.ofp)
    msg.actions.append(of.ofp_action_output(port=dst_port))
    event.connection.send(msg)
