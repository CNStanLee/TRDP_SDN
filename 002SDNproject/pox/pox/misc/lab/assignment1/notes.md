<!--
 * @Author: Changhongli lic9@tcd.com
 * @Date: 2024-03-27 17:18:39
 * @LastEditors: Changhongli lic9@tcd.com
 * @LastEditTime: 2024-04-01 13:55:12
 * @FilePath: /MininetLab/pox/pox/misc/lab/assignment1/notes.md
 * @Description: 
 * 
-->

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