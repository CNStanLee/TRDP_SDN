# SDN2 TRDP OpenFlow Policy Measurement

本文档记录 `002SDNproject/pox/pox/misc/lab/SDN2` 中 d1-d5 防御策略的运行方法与验证结果。

## 测量口径

当前代码只测量控制器侧 `flow_mod` 规则下发时间，即控制器执行 `connection.send(flow_mod)` 循环所消耗的时间。

该时间不包含：

- OpenFlow barrier reply 等待时间
- 交换机确认安装完成时间
- 数据包实际转发/丢弃验证时间

日志关键字为：

```text
POLICY_SEND_TIME
POLICY_SEND_SUMMARY
```

## 环境依赖

Ubuntu 22.04 下可使用：

```sh
sudo apt-get update
sudo apt-get install -y mininet openvswitch-switch openvswitch-testcontroller iperf iproute2
```

确认工具：

```sh
which mn
which ovs-ofctl
systemctl is-active openvswitch-switch
```

本机验证时：

```text
/usr/bin/mn
/usr/bin/ovs-ofctl
openvswitch-switch: active
```

注意：本机默认 `python3` 指向 Anaconda Python，不能导入 Ubuntu apt 安装的 Mininet 模块。因此运行拓扑时使用 `/usr/bin/python3`。

## 运行控制器

终端 1：

```sh
cd ~/prj/TRDP_SDN/002SDNproject/pox
./pox.py log.level --INFO misc.lab.SDN2.controller_trdp
```

控制器监听 POX 默认 OpenFlow 端口 `6633`。拓扑文件中已经显式指定：

```python
net.addController('c0', ip='127.0.0.1', port=6633)
```

## 运行拓扑与自动验证

终端 2：

```sh
cd ~/prj/TRDP_SDN/002SDNproject/pox/pox/misc/lab/SDN2
sudo mn -c
sudo /usr/bin/python3 topo_trdp.py --verify-policies --verify-wait=4
```

`--verify-policies` 会等待策略下发，然后执行：

```sh
sudo ovs-ofctl -O OpenFlow10 dump-flows s1
sudo ovs-ofctl -O OpenFlow10 dump-flows s2
sudo ovs-ofctl -O OpenFlow10 dump-flows s3
sudo ovs-ofctl -O OpenFlow10 dump-flows s4
```

## 策略 Cookie

流表中通过 cookie 区分策略：

| Measure | Cookie | 策略 |
|---|---:|---|
| d1 | `0xd100001` | Creating an ACL |
| d2 | `0xd200001` | Deploying VLAN Trunks for TRDP Communications |
| d3 | `0xd300001` | Adjusting QoS to downgrade priority of malicious packets |
| d4 | `0xd400001` | Restricting traffic on ports of abnormal hosts |
| d5 | `0xd500001` | Isolating ports and preventing data transmission |

基础 TRDP 组播转发规则使用：

```text
0xb000001
```

## 控制器自检

不启动 Mininet 时，可以验证 OpenFlow 规则能否正常生成和打包：

```sh
cd ~/prj/TRDP_SDN/002SDNproject/pox
./pox.py log.level --INFO misc.lab.SDN2.controller_trdp --selftest=True
```

本机自检结果：

| 规则集 | Flow Mods |
|---|---:|
| base TRDP multicast | 56 |
| d1 | 4 |
| d2 | 221 |
| d3 | 4 |
| d4 | 4 |
| d5 | 36 |

## 运行结果

本次 Mininet + OVS 验证结果如下，只统计控制器侧规则下发时间：

| Measure | Description | Cost | Flow Mods | Sent | Switches | Send Time |
|---|---|---:|---:|---:|---:|---:|
| d1 | Creating an ACL | 1.5 | 4 | 4 | 4 | 0.230 ms |
| d2 | Deploying VLAN Trunks for TRDP Communications | 3.3 | 221 | 221 | 4 | 5.124 ms |
| d3 | Adjusting QoS to downgrade priority of malicious packets | 4.6 | 4 | 4 | 4 | 0.183 ms |
| d4 | Restricting traffic on ports of abnormal hosts | 1.8 | 4 | 4 | 4 | 0.200 ms |
| d5 | Isolating ports and preventing data transmission | 8.6 | 36 | 36 | 4 | 0.842 ms |

对应控制器日志：

```text
POLICY_SEND_TIME d1 cost=1.5 flow_mods=4 sent=4 switches=4 elapsed_ms=0.230 description=Creating an ACL
POLICY_SEND_TIME d2 cost=3.3 flow_mods=221 sent=221 switches=4 elapsed_ms=5.124 description=Deploying VLAN Trunks for TRDP Communications
POLICY_SEND_TIME d3 cost=4.6 flow_mods=4 sent=4 switches=4 elapsed_ms=0.183 description=Adjusting QoS to downgrade priority of malicious packets
POLICY_SEND_TIME d4 cost=1.8 flow_mods=4 sent=4 switches=4 elapsed_ms=0.200 description=Restricting traffic on ports of abnormal hosts
POLICY_SEND_TIME d5 cost=8.6 flow_mods=36 sent=36 switches=4 elapsed_ms=0.842 description=Isolating ports and preventing data transmission
POLICY_SEND_SUMMARY_BEGIN
POLICY_SEND_SUMMARY d1 cost=1.5 flow_mods=4 sent=4 switches=4 elapsed_ms=0.230
POLICY_SEND_SUMMARY d2 cost=3.3 flow_mods=221 sent=221 switches=4 elapsed_ms=5.124
POLICY_SEND_SUMMARY d3 cost=4.6 flow_mods=4 sent=4 switches=4 elapsed_ms=0.183
POLICY_SEND_SUMMARY d4 cost=1.8 flow_mods=4 sent=4 switches=4 elapsed_ms=0.200
POLICY_SEND_SUMMARY d5 cost=8.6 flow_mods=36 sent=36 switches=4 elapsed_ms=0.842
POLICY_SEND_SUMMARY_END
```

## 结果解释

d1、d3、d4 都只下发 4 条规则，因此耗时接近，约 `0.2 ms`。

d2 下发 221 条 VLAN trunk 相关规则，因此耗时最高，为 `5.124 ms`。

d5 下发 36 条隔离规则，耗时 `0.842 ms`，位于 4 条规则策略和 221 条规则策略之间。

该结果比 barrier 计时更能反映控制器侧规则下发开销；若需要测量交换机确认完成时间，应重新启用 OpenFlow barrier 计时。

## 退出与清理

停止 POX 控制器：

```sh
Ctrl+C
```

清理 Mininet 状态：

```sh
sudo mn -c
```
