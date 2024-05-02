'''
Author: Changhongli lic9@tcd.com
Date: 2024-04-08 18:13:46
LastEditors: Changhongli lic9@tcd.com
LastEditTime: 2024-04-28 22:23:02
FilePath: /002SDNproject/halosaur/pox/pox/misc/lab/SDN2/topo_trdp.py
Description: 

'''
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time
import os

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




def TrdpTopo():
    net = Mininet( controller=RemoteController)

	# For this part you can reuse the exact same code of the first assignment. Notice that for the links you don't need to have a TCLink with bandwidth limitation for this second part
    info( '*** Adding controller\n' )
	# =>add the controller here
    net.addController('c0')
	
    info( '*** Adding hosts\n' )
    # =>add the hosts here  
    
    # car one node
    h11 = net.addHost('h11', ip=h11_ip, mac=h11_mac)
    h12 = net.addHost('h12', ip=h12_ip, mac=h12_mac)
    h13 = net.addHost('h13', ip=h13_ip, mac=h13_mac)
    h14 = net.addHost('h14', ip=h14_ip, mac=h14_mac)
    h15 = net.addHost('h15', ip=h15_ip, mac=h15_mac)
    h16 = net.addHost('h16', ip=h16_ip, mac=h16_mac)
    h17 = net.addHost('h17', ip=h17_ip, mac=h17_mac)
    h18 = net.addHost('h18', ip=h18_ip, mac=h18_mac)
    h19 = net.addHost('h19', ip=h19_ip, mac=h19_mac)
    
    # car two node
    h21 = net.addHost('h21', ip=h21_ip, mac=h21_mac)
    h22 = net.addHost('h22', ip=h22_ip, mac=h22_mac)
    h23 = net.addHost('h23', ip=h23_ip, mac=h23_mac)
    h24 = net.addHost('h24', ip=h24_ip, mac=h24_mac)
    h25 = net.addHost('h25', ip=h25_ip, mac=h25_mac)
    
    # car three node
    h31 = net.addHost('h31', ip=h31_ip, mac=h31_mac)
    h32 = net.addHost('h32', ip=h32_ip, mac=h32_mac)
    h33 = net.addHost('h33', ip=h33_ip, mac=h33_mac)
    h34 = net.addHost('h34', ip=h34_ip, mac=h34_mac)
    
    # car four node
    h41 = net.addHost('h41', ip=h41_ip, mac=h41_mac)
    h42 = net.addHost('h42', ip=h42_ip, mac=h42_mac)
    h43 = net.addHost('h43', ip=h43_ip, mac=h43_mac)
    h44 = net.addHost('h44', ip=h44_ip, mac=h44_mac)
    h45 = net.addHost('h45', ip=h45_ip, mac=h45_mac)
    
	
    info( '*** Adding switches\n' )
	# =>add the switch here
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')
	
    info( '*** Creating links\n' )
	# =>create the links here. You don't need to have a TCLink with bandwidth limitation for this second part
    net.addLink(h11, s1, port1=1, port2=1)
    net.addLink(h12, s1, port1=1, port2=2)
    net.addLink(h13, s1, port1=1, port2=3)
    net.addLink(h14, s1, port1=1, port2=4)
    net.addLink(h15, s1, port1=1, port2=5)
    net.addLink(h16, s1, port1=1, port2=6)
    net.addLink(h17, s1, port1=1, port2=7)
    net.addLink(h18, s1, port1=1, port2=8)
    net.addLink(h19, s1, port1=1, port2=9)
    
    net.addLink(h21, s2, port1=1, port2=1)
    net.addLink(h22, s2, port1=1, port2=2)
    net.addLink(h23, s2, port1=1, port2=3)
    net.addLink(h24, s2, port1=1, port2=4)
    net.addLink(h25, s2, port1=1, port2=5)
    
    net.addLink(h31, s3, port1=1, port2=1)
    net.addLink(h32, s3, port1=1, port2=2)
    net.addLink(h33, s3, port1=1, port2=3)
    net.addLink(h34, s3, port1=1, port2=4)
    
    net.addLink(h41, s4, port1=1, port2=1)
    net.addLink(h42, s4, port1=1, port2=2)
    net.addLink(h43, s4, port1=1, port2=3)
    net.addLink(h44, s4, port1=1, port2=4)
    net.addLink(h45, s4, port1=1, port2=5)
    
    net.addLink(s1, s2, port1=12, port2=11)
    net.addLink(s1, s3, port1=13, port2=11)
    net.addLink(s1, s4, port1=14, port2=11)
    
    net.addLink(s2, s3, port1=13, port2=12)
    net.addLink(s2, s4, port1=14, port2=12)
    
    net.addLink(s3, s4, port1=14, port2=13)
    
    
    # add the links between the switches

    
    # =>start the network
    info( '*** Starting network\n')
    net.start()
    h11, h12, h13, h14, h15, h16, h17, h18, h19 = net.hosts[0], net.hosts[1], net.hosts[2], net.hosts[3], net.hosts[4], net.hosts[5], net.hosts[6], net.hosts[7], net.hosts[8]
    h21, h22, h23, h24, h25 = net.hosts[9], net.hosts[10], net.hosts[11], net.hosts[12], net.hosts[13]
    h31, h32, h33, h34 = net.hosts[14], net.hosts[15], net.hosts[16], net.hosts[17]
    h41, h42, h43, h44, h45 = net.hosts[18], net.hosts[19], net.hosts[20], net.hosts[21], net.hosts[22]
    
    
    
    
    # check ports
    os.system('sudo ovs-vsctl show')
    
    # =>add the queues and QoS
    # os.system('sudo ovs-vsctl -- set Port s1-eth3 qos=@newqos  \
    #        -- --id=@newqos create QoS type=linux-htb other-config:max-rate=100000000000 queues=0=@q0,1=@q1 \
    #        -- --id=@q0 create Queue other-config:min-rate=20000000: other-config:max-rate=50000000\
    #        -- --id=@q1 create Queue other-config:min-rate=50000000: other-config:max-rate=100000000')  # fill in here command to add two queues to port 3 of the switch: Q0 with min rate 20000000 and max rate -SELECT THE PROPER RATE-, Q1 with min rate 50000000 and max rate -SELECT THE PROPER RATE-

    # os.system('sudo ovs-vsctl -- set Port s1-eth4 qos=@newqos \
    #        -- --id=@newqos create QoS type=linux-htb other-config:max-rate=100000000000 queues=2=@q2 \
    #        -- --id=@q2 create Queue other-config:min-rate=20000000: other-config:max-rate=500000000')
    

# Don't modify the code below, these will test your controller

    h11.cmd('iperf -s &')
    time.sleep(1)

    info( '\n\n\n\n*** Testing PIR from H1 to H3\n')
    print(h12.cmd('iperf -c %s' % h11.IP()))
    time.sleep(1)

    info( '\n\n\n\n*** Testing CIR to H2 to H3\n')
    print(h13.cmd('iperf -c %s' % h11.IP()))
    time.sleep(1)
    
    # send the python script to the broadcast ip
    # os.system('sudo mnexec -a %s python /home/lic9/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN/app.py %s %s &' % (h11.name, bc11, 30))
    # os.system('sudo mnexec -a %s python /home/lic9/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN/app.py %s %s &' % (h12.name, bc12, 30))
    # os.system('sudo mnexec -a %s python /home/lic9/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN/app.py %s %s &' % (h13.name, bc13, 30))
    # os.system('sudo mnexec -a %s python /home/lic9/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN/app.py %s %s &' % (h14.name, bc14, 30))
    # os.system('sudo mnexec -a %s python /home/lic9/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN/app.py %s %s &' % (h15.name, bc15, 30))
    # os.system('sudo mnexec -a %s python /home/lic9/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN/app.py %s %s &' % (h16.name, bc16, 100))
    # os.system('sudo mnexec -a %s python /home/lic9/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN/app.py %s %s &' % (h17.name, bc17, 200))
    # os.system('sudo mnexec -a %s python /home/lic9/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN/app.py %s %s &' % (h18.name, bc18, 50))
    # os.system('sudo mnexec -a %s python /home/lic9/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN/app.py %s %s &' % (h19.name, bc19, 50))
    
    # os.system('sudo mnexec -a %s python /home/lic9/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN/app.py %s %s &' % (h21.name, bc21, 30))
    # os.system('sudo mnexec -a %s python /home/lic9/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN/app.py %s %s &' % (h22.name, bc22, 30))
    # os.system('sudo mnexec -a %s python /home/lic9/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN/app.py %s %s &' % (h23.name, bc23, 30))
    # os.system('sudo mnexec -a %s python /home/lic9/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN/app.py %s %s &' % (h24.name, bc24, 30))
    # os.system('sudo mnexec -a %s python /home/lic9/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN/app.py %s %s &' % (h25.name, bc25, 100))
    
    # os.system('sudo mnexec -a %s python /home/lic9/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN/app.py %s %s &' % (h31.name, bc31, 30))
    # os.system('sudo mnexec -a %s python /home/lic9/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN/app.py %s %s &' % (h32.name, bc32, 30))
    # os.system('sudo mnexec -a %s python /home/lic9/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN/app.py %s %s &' % (h33.name, bc33, 30))
    # os.system('sudo mnexec -a %s python /home/lic9/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN/app.py %s %s &' % (h34.name, bc34, 100))
    
    # os.system('sudo mnexec -a %s python /home/lic9/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN/app.py %s %s &' % (h41.name, bc41, 30))
    # os.system('sudo mnexec -a %s python /home/lic9/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN/app.py %s %s &' % (h42.name, bc42, 30))
    # os.system('sudo mnexec -a %s python /home/lic9/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN/app.py %s %s &' % (h43.name, bc43, 30))
    # os.system('sudo mnexec -a %s python /home/lic9/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN/app.py %s %s &' % (h44.name, bc44, 30))
    # os.system('sudo mnexec -a %s python /home/lic9/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN/app.py %s %s &' % (h45.name, bc45, 100))
    
    
    CLI( net )
    # os.system('sudo ovs-vsctl clear Port s1-eth3 qos')
    # os.system('sudo ovs-vsctl clear Port s1-eth4 qos')

    os.system('sudo ovs-vsctl --all destroy qos')
    os.system('sudo ovs-vsctl --all destroy queue')
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    TrdpTopo()

