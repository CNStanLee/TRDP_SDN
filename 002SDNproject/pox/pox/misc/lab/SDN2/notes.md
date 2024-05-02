<!--
 * @Author: Changhongli lic9@tcd.com
 * @Date: 2024-03-27 17:18:39
 * @LastEditors: Changhongli lic9@tcd.com
 * @LastEditTime: 2024-04-28 21:13:34
 * @FilePath: /pox/pox/misc/lab/SDN2/notes.md
 * @Description: 
 * 
-->

# Assignment1

### Run the Controller
```sh
cd ~/prj/TRDP_SDN/002SDNproject/pox
./pox.py log.level --DEBUG misc.lab.SDN2.controller_trdp
```
### Run the Mininet Topo
```sh
cd ~/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN2/
sudo python3 topo_trdp.py
```
### Kill the thread if controller is not closed correctly
```sh
ps -aux | grep pox
kill 1234
```