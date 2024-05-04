<!--
 * @Author: Changhongli lic9@tcd.com
 * @Date: 2024-03-27 17:18:39
 * @LastEditors: Changhongli lic9@tcd.com
 * @LastEditTime: 2024-04-28 22:12:09
 * @FilePath: /002SDNproject/halosaur/pox/pox/misc/lab/SDN2/notes.md
 * @Description: 
 * 
-->

# Assignment1

### Run the Controller
```sh
cd ~/projects/TrdpSdn/TRDP_SDN/002SDNproject/halosaur/pox
./pox.py log.level --DEBUG misc.lab.SDN2.controller_trdp
```
### Run the Mininet Topo
```sh
cd ~/projects/TrdpSdn/TRDP_SDN/002SDNproject/halosaur/pox/pox/misc/lab/SDN2/
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