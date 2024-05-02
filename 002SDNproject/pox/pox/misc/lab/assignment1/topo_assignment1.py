from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import time
import os

def assignmentTopo():
    net = Mininet( controller=RemoteController)

    info( '*** Adding controller\n' )
	# =>add the controller here
    net.addController('c0')
	
    info( '*** Adding hosts\n' )
	# =>h1 is already added, now add the other hosts here
    h1 = net.addHost( 'h1', ip='10.0.0.2', mac='00:00:00:00:00:02' )
    h2 = net.addHost( 'h2', ip='10.0.0.3', mac='00:00:00:00:00:03' )
    h3 = net.addHost( 'h3', ip='10.0.0.4', mac='00:00:00:00:00:04' )
    h4 = net.addHost( 'h4', ip='10.0.0.5', mac='00:00:00:00:00:05' )
	
    info( '*** Adding switches\n' )
	# =>add the switch here
    s1 = net.addSwitch('s1')
	
	
    info( '*** Creating links\n' )
	# =>create the links here
    #net.addLink( h1, s1, cls = TCLink, bw = 250 )
    net.addLink( h1, s1)     
    net.addLink( h2, s1)
    net.addLink( h3, s1)
    net.addLink( h4, s1)
   


    info( '*** Starting network\n')
    net.start()
    h1, h2, h3, h4 = net.hosts[0],net.hosts[1],net.hosts[2],net.hosts[3]
    
    command_dst1 = "sudo ovs-vsctl set port s1-eth1 qos=@newqos1 -- \
    --id=@newqos1 create qos type=linux-htb \
    queues=0=@q10,1=@q11,2=@q12,3=@q13,5=@q15 -- \
    -- --id=@q10 create queue other-config:min-rate=20000000 other-config:max-rate=50000000\
    -- --id=@q11 create queue other-config:min-rate=20000000 other-config:max-rate=100000000\
    -- --id=@q12 create queue other-config:min-rate=20000000 other-config:max-rate=500000000\
    -- --id=@q15 create queue other-config:min-rate=20000000 other-config:max-rate=250000000\
    -- --id=@q13 create queue other-config:min-rate=20000000 other-config:max-rate=0"
    
    command_dst2 = "sudo ovs-vsctl set port s1-eth2 qos=@newqos2 -- \
    --id=@newqos2 create qos type=linux-htb \
    queues=0=@q20,1=@q21,2=@q22,3=@q23,5=@q25 -- \
    -- --id=@q20 create queue other-config:min-rate=20000000 other-config:max-rate=50000000\
    -- --id=@q21 create queue other-config:min-rate=20000000 other-config:max-rate=100000000\
    -- --id=@q22 create queue other-config:min-rate=20000000 other-config:max-rate=500000000\
    -- --id=@q25 create queue other-config:min-rate=20000000 other-config:max-rate=250000000\
    -- --id=@q23 create queue other-config:min-rate=20000000 other-config:max-rate=0"
    
    command_dst3 = "sudo ovs-vsctl set port s1-eth3 qos=@newqos3 -- \
    --id=@newqos3 create qos type=linux-htb \
    queues=0=@q30,1=@q31,2=@q32,3=@q33,5=@q35 -- \
    -- --id=@q30 create queue other-config:min-rate=20000000 other-config:max-rate=50000000\
    -- --id=@q31 create queue other-config:min-rate=20000000 other-config:max-rate=100000000\
    -- --id=@q32 create queue other-config:min-rate=20000000 other-config:max-rate=500000000\
    -- --id=@q35 create queue other-config:min-rate=20000000 other-config:max-rate=250000000\
    -- --id=@q33 create queue other-config:min-rate=20000000 other-config:max-rate=0"
    
    command_dst4 = "sudo ovs-vsctl set port s1-eth4 qos=@newqos4 -- \
    --id=@newqos4 create qos type=linux-htb \
    queues=0=@q40,1=@q41,2=@q42,3=@q43,5=@q45 -- \
    -- --id=@q40 create queue other-config:min-rate=20000000 other-config:max-rate=50000000\
    -- --id=@q41 create queue other-config:min-rate=20000000 other-config:max-rate=100000000\
    -- --id=@q42 create queue other-config:min-rate=20000000 other-config:max-rate=500000000\
    -- --id=@q45 create queue other-config:min-rate=20000000 other-config:max-rate=250000000\
    -- --id=@q43 create queue other-config:min-rate=20000000 other-config:max-rate=0"
    
    
    
    os.system(command_dst1)
    time.sleep(1)
    os.system(command_dst2)
    time.sleep(1)
    os.system(command_dst3)
    time.sleep(1)
    os.system(command_dst4)
    time.sleep(1)


 
    # Don't modify the code below, these will test your controller
# ------------------------------------------------------------------------------------------- #
# h3
# ------------------------------------------------------------------------------------------- #
    h3.cmd('iperf -s &')
    time.sleep(1)

    info( '\n\n\n\n*** Testing PIR from H1 to H3\n')
    print(h1.cmd('iperf -c %s' % h3.IP()))
    time.sleep(1)

    info( '\n\n\n\n*** Testing CIR to H2 to H3\n')
    print(h2.cmd('iperf -c %s' % h3.IP()))
    time.sleep(1)
# ------------------------------------------------------------------------------------------- #
# h1
# ------------------------------------------------------------------------------------------- #
    h1.cmd('iperf -s &')
    time.sleep(1)
    
    info( '\n\n\n\n*** Testing CIR to H3 to H1\n')
    print(h3.cmd('iperf -c %s' % h1.IP()))
    time.sleep(1)
# ------------------------------------------------------------------------------------------- #
# h2
# ------------------------------------------------------------------------------------------- #
    h2.cmd('iperf -s &')
    time.sleep(1)
    
    info( '\n\n\n\n*** Testing CIR to H3 to H2\n')
    print(h3.cmd('iperf -c %s' % h2.IP()))
    time.sleep(1)
# ------------------------------------------------------------------------------------------- #
# h4
# ------------------------------------------------------------------------------------------- #
    h4.cmd('iperf -s &')
    time.sleep(1)
    
    info( '\n\n\n\n*** Testing CIR to H1 to H4\n')
    print(h1.cmd('iperf -c %s' % h4.IP()))
    time.sleep(1)

    info( '\n\n\n\n*** Testing CIR to H2 to H4\n')
    print(h2.cmd('iperf -c %s' % h4.IP()))
    time.sleep(1)

    info( '\n\n\n\n*** Testing CIR to H3 to H4\n')
    print(h3.cmd('iperf -c %s' % h4.IP()))
    time.sleep(1)
# ------------------------------------------------------------------------------------------- #
# h1 & h2
# ------------------------------------------------------------------------------------------- #
    info( '\n\n\n\n*** Testing CIR to H1 to H2\n')
    print(h1.cmd('iperf -c %s' % h2.IP()))
    time.sleep(1)

    info( '\n\n\n\n*** Testing CIR to H2 to H1\n')
    print(h2.cmd('iperf -c %s' % h1.IP()))
    time.sleep(1)
# ------------------------------------------------------------------------------------------- #
# Test timeout
# ------------------------------------------------------------------------------------------- #
    # h3.cmd('iperf -s &')
    # time.sleep(1)
    
    # info( '\n\n\n\n*** Testing CIR to H2 to H3\n')
    # info( '\n\n\n\n*** Testing Timeout\n')
    # print(h2.cmd('iperf -c %s' % h3.IP()))
    
    info( '\n\n\n\n*** Current Rules(0/50s)\n')
    os.system("sudo ovs-ofctl dump-flows s1")
    info( '\n\n\n\n*** Please Wait\n')
    time.sleep(20)

    info( '\n\n\n\n*** Current Rules(20/50s)\n')
    os.system("sudo ovs-ofctl dump-flows s1")
    info( '\n\n\n\n*** Please Wait\n')
    time.sleep(20)
    
    info( '\n\n\n\n*** Current Rules(40/50s)\n')
    os.system("sudo ovs-ofctl dump-flows s1")
    info( '\n\n\n\n*** Please Wait\n')
    time.sleep(10)
    
    info( '\n\n\n\n*** Current Rules(50/50s)\n')
    os.system("sudo ovs-ofctl dump-flows s1")
    

# ------------------------------------------------------------------------------------------- #
# release
# ------------------------------------------------------------------------------------------- #
    info( '*** Running CLI\n' )
    CLI( net )
    os.system('sudo ovs-vsctl clear Port s1-eth1 qos')
    os.system('sudo ovs-vsctl clear Port s1-eth2 qos')
    os.system('sudo ovs-vsctl clear Port s1-eth3 qos')
    os.system('sudo ovs-vsctl clear Port s1-eth4 qos')
    os.system('sudo ovs-vsctl --all destroy qos')
    os.system('sudo ovs-vsctl --all destroy queue')
    info( '*** Stopping network' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    assignmentTopo()
