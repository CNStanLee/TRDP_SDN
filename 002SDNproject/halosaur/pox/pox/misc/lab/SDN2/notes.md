<!--
 * @Author: Changhongli lic9@tcd.com
 * @Date: 2024-03-27 17:18:39
 * @LastEditors: Changhongli lic9@tcd.com
 * @LastEditTime: 2024-05-07 16:02:05
 * @FilePath: /TRDP_SDN/002SDNproject/halosaur/pox/pox/misc/lab/SDN2/notes.md
 * @Description: 
 * 
-->

### Run the Controller
```sh
cd ~/projects/TrdpSdn/TRDP_SDN/002SDNproject/halosaur/pox
./pox.py log.level --DEBUG misc.lab.SDN2.controller_trdp

cd ~/prj/TRDP_SDN/002SDNproject/halosaur/pox
./pox.py log.level --DEBUG misc.lab.SDN2.controller_trdp


cd ~/projects/TRDP_SDN/002SDNproject/halosaur/pox
./pox.py log.level --DEBUG misc.lab.SDN2.controller_trdp
```
### Run the Mininet Topo
```sh
cd ~/projects/TrdpSdn/TRDP_SDN/002SDNproject/halosaur/pox/pox/misc/lab/SDN2/
sudo python3 topo_trdp.py

cd ~/prj/TRDP_SDN/002SDNproject/halosaur/pox/pox/misc/lab/SDN2/
sudo python3 topo_trdp.py

cd ~/projects/TRDP_SDN/002SDNproject/halosaur/pox/pox/misc/lab/SDN2/
sudo python3 topo_trdp.py
```
### Kill the thread if controller is not closed correctly
```sh
ps -aux | grep pox
kill 1234
```

sudo smcroutectl show interfaces
sudo smcroutectl show interfaces
sudo systemctl restart smcroute

### broadcast problem
```sh
sudo sysctl -w net.ipv4.conf.all.mc_forwarding=1
sudo gedit /etc/sysctl.conf
net.ipv4.conf.all.mc_forwarding=1

systemctl stop firewalld
service iptables stop

sudo sysctl -w net.ipv4.conf.en4.rp_filter=0
sudo sysctl -w net.ipv4.conf.all.rp_filter=0

```sh

sudo sysctl net.ipv4.ip_forward=1
sysctl net.ipv4.ip_forward

turn off ufw
sudo ufw disable
sudo ufw enable


dst net 239.255.0.0 mask 255.255.0.0 and udp
iptables -A INPUT -d 239.255.0.0/16 -p udp --dport 1900 -j DROP

### wireshark filter
udp and dst net 239.255.0.0 mask 255.255.0.0 and not port 1900
60s

