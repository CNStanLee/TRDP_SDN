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
The controller now installs TRDP forwarding rules and measures only the
controller-side flow_mod send time for d1-d5 policies. Look for:
```text
POLICY_SEND_TIME d1 ... elapsed_ms=...
POLICY_SEND_TIME d2 ... elapsed_ms=...
POLICY_SEND_TIME d3 ... elapsed_ms=...
POLICY_SEND_TIME d4 ... elapsed_ms=...
POLICY_SEND_TIME d5 ... elapsed_ms=...
```

### Run the Mininet Topo
```sh
cd ~/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN2/
sudo /usr/bin/python3 topo_trdp.py
```
### Run Automated Policy Verification
Start the controller first, then run:
```sh
cd ~/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN2/
sudo /usr/bin/python3 topo_trdp.py --verify-policies --verify-wait=6
```
This waits for policy deployment and dumps the OpenFlow tables for s1-s4. The
policy cookies are:
```text
d1 0xd100001
d2 0xd200001
d3 0xd300001
d4 0xd400001
d5 0xd500001
```

### Controller Self-Test Without Mininet
```sh
cd ~/prj/TRDP_SDN/002SDNproject/pox
./pox.py log.level --INFO misc.lab.SDN2.controller_trdp --selftest=True
```
### Kill the thread if controller is not closed correctly
```sh
ps -aux | grep pox
kill 1234
```
