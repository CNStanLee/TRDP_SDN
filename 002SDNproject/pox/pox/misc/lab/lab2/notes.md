<!--
 * @Author: Changhongli lic9@tcd.com
 * @Date: 2024-03-27 17:18:39
 * @LastEditors: Changhongli lic9@tcd.com
 * @LastEditTime: 2024-03-30 15:11:25
 * @FilePath: /MininetLab/pox/pox/misc/lab/lab2/notes.md
 * @Description: 
 * 
-->
# Lab2
## Part1
### Run the Controller
```sh
cd ~/prj/MininetLab/pox
./pox.py log.level --DEBUG misc.lab.lab2.simple_controller
```
### Run the Mininet Topo
```sh
cd ~/prj/MininetLab/pox/pox/misc/lab/lab2
sudo python3 tree0.py
```
### Test the firewall application against the topology
```sh
mininet> pingall
*** Ping: testing ping reachability
h1 -> X h3 h4
h2 -> X h3 h4
h3 -> h1 h2 X
h4 -> h1 h2 X
*** Results: 33% dropped (8/12 received)
```
### insect s1 with openflow

* cookie: 用于识别流表项的唯一标识符。
* duration: 流表项已经存在的时间。
* table: 流表项所属的表编号。
* n_packets: 匹配到该流表项的数据包数量。
* n_bytes: 匹配到该流表项的总字节数。
* priority: 流表项的优先级。
* dl_src: 源 MAC 地址匹配条件。
* dl_dst: 目标 MAC 地址匹配条件。
* actions: 匹配到流表项后需要执行的动作，如输出到指定端口。

```sh
mininet@mininet-vm:~$ sudo ovs-ofctl dump-flows s1
cookie=0x0, duration=171.743s, table=0, n_packets=27, n_bytes=2142,
priority=32000,dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:02 actions=drop
cookie=0x0, duration=171.742s, table=0, n_packets=0, n_bytes=0,
priority=32000,dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:04 actions=drop
cookie=0x0, duration=113.474s, table=0, n_packets=0, n_bytes=0,
priority=100,dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:02
actions=output:"s1-eth2"
cookie=0x0, duration=113.474s, table=0, n_packets=12, n_bytes=728,
priority=100,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:01
actions=output:"s1-eth1"
cookie=0x0, duration=72.563s, table=0, n_packets=6, n_bytes=532,
priority=100,dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:03
actions=output:"s1-eth3"
cookie=0x0, duration=72.563s, table=0, n_packets=7, n_bytes=574,
priority=100,dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:01
actions=output:"s1-eth1"
cookie=0x0, duration=54.864s, table=0, n_packets=3, n_bytes=238,
priority=100,dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:04
actions=output:"s1-eth3"cookie=0x0, duration=54.864s, table=0, n_packets=4, n_bytes=280,
priority=100,dl_src=00:00:00:00:00:04,dl_dst=00:00:00:00:00:01
actions=output:"s1-eth1"
cookie=0x0, duration=44.847s, table=0, n_packets=3, n_bytes=238,
priority=100,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:03
actions=output:"s1-eth3"
cookie=0x0, duration=44.847s, table=0, n_packets=4, n_bytes=280,
priority=100,dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:02
actions=output:"s1-eth2"
cookie=0x0, duration=44.832s, table=0, n_packets=3, n_bytes=238,
priority=100,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:04
actions=output:"s1-eth3"
cookie=0x0, duration=44.832s, table=0, n_packets=4, n_bytes=280,
priority=100,dl_src=00:00:00:00:00:04,dl_dst=00:00:00:00:00:02
actions=output:"s1-eth2"
```
## Part2

### Create Topo
```sh
sudo -E mn --topo single,3 --switch ovsk --controller remote --mac
```
### verify the topology
```sh
mininet> links
h1-eth0<->s1-eth1 (OK OK)
h2-eth0<->s1-eth2 (OK OK)
h3-eth0<->s1-eth3 (OK OK)
```
### verify the ports 
```sh
sudo ovs-vsctl show
```
result will be like
```sh
e7a21c84-4464-4b53-9d84-7ac031b48c46
Bridge s1
Controller "ptcp:6654"
Controller "tcp:127.0.0.1:6653"
fail_mode: secure
Port s1-eth2
Interface s1-eth2
Port s1-eth1
Interface s1-eth1
Port s1-eth3
Interface s1-eth3
Port s1
Interface s1
type: internal
ovs_version: "2.13.1"
```
### Simple forwarding rules
Add simple forwarding rules
```sh
sudo ovs-ofctl add-flow s1 dl_type=0x806,actions=output:all
sudo ovs-ofctl add-flow s1 dl_dst=00:00:00:00:00:02,actions=output:\"s1-eth2\"
sudo ovs-ofctl add-flow s1 dl_dst=00:00:00:00:00:01,actions=output:\"s1-eth1\"
sudo ovs-ofctl add-flow s1 dl_dst=00:00:00:00:00:03,actions=output:\"s1-eth3\"
```
Run iperf to check
```sh
mininet> h3 iperf -s &
mininet> h1 iperf -c 10.0.0.3
mininet> h2 iperf -c 10.0.0.3
```
Result will be like
```sh
------------------------------------------------------------
Client connecting to 10.0.0.3, TCP port 5001
TCP window size: 1.38 MByte (default)
------------------------------------------------------------
[ 3] local 10.0.0.2 port 45796 connected with 10.0.0.3 port 5001
[ ID] Interval Transfer Bandwidth
[ 3] 0.0-10.0 sec 14.7 GBytes 12.6 Gbits/sec
```
rate around 10G
### Adding QOS Rules
We can now shape the traffic using queues at the ingress port to the switches.

In this instance, we create two queues for the port connected to h3. 

In one we set maximum rate to 500Mbps and minimum rate to 200Mbps.


On the other set we set maximum rate to 100 Mbps and minimum rate to 50Mbps.
\\
```sh
sudo ovs-vsctl set port s1-eth3 \
qos=@newqos \
-- --id=@newqos \
create qos \
type=linux-htb \
queues=0=@q0,1=@q1 \
-- --id=@q0 \
create queue \
other-config:min-rate=200000000 \
other-config:max-rate=500000000 \
-- --id=@q1 \
create queue \
other-config:min-rate=50000000 \
other-config:max-rate=100000000
```
Notice that the firsto queue ID is 0, the second is 1. These are the IDs you will use in the flow rule.
```sh
sudo ovs-ofctl del-flows s1 out_port=3 # delete the flow rule towards h3
sudo ovs-ofctl add-flow s1
dl_dst=00:00:00:00:00:03,dl_src=00:00:00:00:00:01,actions=enqueue:3:0
sudo ovs-ofctl add-flow s1
dl_dst=00:00:00:00:00:03,dl_src=00:00:00:00:00:02,actions=enqueue:3:1
```
Apply the rules, notice , 3:0 means port 3, queues0 corresponding q0


In python file, use below instead
```sh
os.system(‘COMMAND’)
flow.actions.append(of.ofp_action_enqueue(port = ...variable identifying the
destination port...,queue_id= ...variable identifying the queue id... )
```
### Check QOS Rules
Check Qos Rules of the port
```sh
sudo ovs-vsctl list Port s1-eth3
```
Check all qos rules
```sh
sudo ovs-vsctl list qos
```
and the corresponding queues by typing
```sh
sudo ovs-vsctl list queue
```
Remove Qos Rules from the obj
```sh
sudo ovs-vsctl clear Port s1-eth3 qos
```
Destroy Qos Ruels
```sh
sudo ovs-vsctl destroy qos 60f547c9-d672-4090-b22b-c8d2b19d4a01
sudo ovs-vsctl --all destroy qos
```
Destroy Qos Queues
```sh
mininet > sudo ovs-vsctl destroy queue 20491d88-0614-45eb-82cc-
f2bcf1bff77b 76b55b3d-3973-4fec-9abc-5973d6adcd57
mininet > sudo ovs-vsctl --all destroy queue
```
### Meters
#### Topo
```sh
         C1
         |
     H1--S1--H2
```
```sh
sudo -E mn --switch ovsk --controller remote --mac
```
#### Adding flows and rules
```sh
$ sudo ovs-ofctl del-flows s1
$ sudo ovs-ofctl -O OpenFlow13 del-meter s1 meter=1
```
mannually insert meter rules
 ```sh
$ sudo ovs-ofctl -O OpenFlow13 add-meter s1
meter=1,kbps,band=type=drop,rate=30000
$ sudo ovs-ofctl -O OpenFlow13 add-flow s1
in_port=1,priority=100,actions=meter:1,output:2
$ sudo ovs-ofctl -O OpenFlow13 add-flow s1
in_port=2,priority=100,actions=output:1
```
#### Testing
 ```sh
mininet> h2 iperf -s &
mininet> h1 iperf -c 10.0.0.2
```
modify the meter and run again
 ```sh
sudo ovs-ofctl -O OpenFlow13 mod-meter s1
meter=1,kbps,band=type=drop,rate=300000
```
#### Validating and debugging
 ```sh
$ sudo ovs-ofctl -O OpenFlow13 meter-stats s1

OFPST_METER reply (OF1.3) (xid=0x2):
meter:1 flow_count:1 packet_in_count:4374 byte_in_count:50483292
duration:586.887s bands:
0: packet_count:353 byte_count:4867026
```
 ```sh
sudo ovs-ofctl -O OpenFlow13 meter-features s1

OFPST_METER_FEATURES reply (OF1.3) (xid=0x2):
max_meter:4294967295 max_bands:1 max_color:0
band_types: drop
capabilities: kbps pktps burst stats

```
# Assignment1

### Run the Controller
```sh
cd ~/prj/MininetLab/pox
./pox.py log.level --DEBUG misc.lab.assignment1.controller_assignment1
```
### Run the Mininet Topo
```sh
cd ~/prj/MininetLab/pox/pox/misc/lab/assignment1/
sudo python3 topo_assignment1.py
```
### Kill the thread if controller is not closed correctly
```sh
ps -aux | grep pox
kill 1234
```