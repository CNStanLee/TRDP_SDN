from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time
import os

def assignmentTopo():
    net = Mininet( controller=RemoteController )

	# For this part you can reuse the exact same code of the first assignment. Notice that for the links you don't need to have a TCLink with bandwidth limitation for this second part
    info( '*** Adding controller\n' )
	# =>add the controller here
    net.addController('c0')

    info( '*** Adding hosts\n' )
    h1 = net.addHost( 'h1', ip='10.0.0.1', mac='00:00:00:00:00:01' )
    h2 = net.addHost( 'h2', ip='10.0.0.2', mac='00:00:00:00:00:02' )
    h3 = net.addHost( 'h3', ip='10.0.0.3', mac='00:00:00:00:00:03' )
    h4 = net.addHost( 'h4', ip='10.0.0.4', mac='00:00:00:00:00:04' )
	# =>h1 is already added, now add the other hosts here
	
	
    info( '*** Adding switches\n' )
	# =>add the switch here
    s1 = net.addSwitch('s1')
	
    info( '*** Creating links\n' )
	# =>create the links here. You don't need to have a TCLink with bandwidth limitation for this second part
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    net.addLink(h4, s1)


    info( '*** Starting network\n')
    net.start()
    h1, h2, h3, h4 = net.hosts[0],net.hosts[1],net.hosts[2],net.hosts[3]

    os.system('sudo ovs-vsctl -- set Port s1-eth3 qos=@newqos  \
           -- --id=@newqos create QoS type=linux-htb other-config:max-rate=100000000000 queues=0=@q0,1=@q1 \
           -- --id=@q0 create Queue other-config:min-rate=20000000: other-config:max-rate=50000000\
           -- --id=@q1 create Queue other-config:min-rate=50000000: other-config:max-rate=100000000')  # fill in here command to add two queues to port 3 of the switch: Q0 with min rate 20000000 and max rate -SELECT THE PROPER RATE-, Q1 with min rate 50000000 and max rate -SELECT THE PROPER RATE-

    os.system('sudo ovs-vsctl -- set Port s1-eth4 qos=@newqos \
           -- --id=@newqos create QoS type=linux-htb other-config:max-rate=100000000000 queues=2=@q0 \
           -- --id=@q0 create Queue other-config:min-rate=20000000: other-config:max-rate=500000000')


# Don't modify the code below, these will test your controller

    info( '\n\n\n\n*** Testing CIR from H1 to H3 port 30 - should be capped at 50Mb/s\n')
    h3.cmd('iperf -s -p 30 &')
    print(h1.cmd('iperf -c %s -p 30' % h3.IP()))
    time.sleep(1)
    
    info( '\n\n\n\n*** Testing CIR from H2 to H3 port 30 - should be blocked \n')
    print(h2.cmd('iperf -c %s -p 30' % h3.IP()))
    time.sleep(1)

    info( '\n\n\n\n*** Testing CIR from H2 to H3 port 50 - should be capped at 100Mb/s\n')
    h3.cmd('iperf -s -p 50 &')
    print(h2.cmd('iperf -c %s -p 50' % h3.IP()))
    time.sleep(1)
    
    info( '\n\n\n\n*** Testing link from H1 to H3 on port 20 - should be blocked\n')
    h3.cmd('iperf -s -p 20 &')
    print(h1.cmd('iperf -c %s -p 20' % h3.IP()))
    time.sleep(1)


    info( '\n\n\n\n*** Testing CIR from H1 to H4 port 80 - should not be capped\n')
    h4.cmd('iperf -s -p80 &')
    print(h1.cmd('iperf -c %s -p80' % h4.IP()))
    time.sleep(1)

    info( '\n\n\n\n*** Testing CIR from H2 to H4 port 80 - should not be capped\n')
    print(h2.cmd('iperf -c %s -p80' % h4.IP()))
    time.sleep(1)
    
    info( '\n\n\n\n*** Testing CIR from H3 to H4 port 90 - should be capped at 500Mb/s\n')
    h4.cmd('iperf -s -p90 &')
    print(h3.cmd('iperf -c %s -p90' % h4.IP()))
    time.sleep(1)
    
    info( '\n\n\n\n*** Testing link from H2 to H4 port 90 - should be blocked\n')
    print(h2.cmd('iperf -c %s -p90' % h4.IP()))
    time.sleep(1)
    
    info( '\n\n\n\n*** Testing link from H1 to H2 - should bot be capped\n')
    h2.cmd('iperf -s &')
    print(h1.cmd('iperf -c%s' % h2.IP()))
    time.sleep(1)

    CLI( net )
    os.system('sudo ovs-vsctl clear Port s1-eth3 qos')
    os.system('sudo ovs-vsctl clear Port s1-eth4 qos')
    os.system('sudo ovs-vsctl --all destroy qos')
    os.system('sudo ovs-vsctl --all destroy queue')
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    assignmentTopo()



