<!--
 * @Author: Changhongli lic9@tcd.com
 * @Date: 2024-03-27 17:18:39
 * @LastEditors: Changhongli lic9@tcd.com
 * @LastEditTime: 2024-04-09 15:17:37
 * @FilePath: /MininetLab/pox/pox/misc/lab/assignment2/notes.md
 * @Description: 
 * 
-->

# Assignment1

### Run the Controller
```sh
cd ~/prj/MininetLab/pox
./pox.py log.level --DEBUG misc.lab.assignment2.controller_assignment2
```
### Run the Mininet Topo
```sh
cd ~/prj/MininetLab/pox/pox/misc/lab/assignment2/
sudo python3 topo_assignment2.py
```
### Kill the thread if controller is not closed correctly
```sh
ps -aux | grep pox
kill 1234
```