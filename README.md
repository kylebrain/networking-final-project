[![build](https://img.shields.io/github/workflow/status/kylebrain/networking-final-project/Build%20Test%20Deploy)](https://github.com/kylebrain/networking-final-project/actions)
[![coverage](https://img.shields.io/codecov/c/github/kylebrain/networking-final-project)](https://codecov.io/gh/kylebrain/networking-final-project)
# Distributed Load Routing v1.0.4
Simulates a network and runs a networking protocol aimed to distribute packet load in order to distribute battery depletion.

## Installation
```bash
pip install load-distributed-routing
```

## Package Link PyPi
[Release](https://pypi.org/project/load-distributed-routing/)\
[Development](https://test.pypi.org/project/load-distributed-routing/)

## Configuration File

| Field | Description | Accepted Values |
| ----- |------------ | --------------- |
| num_nodes | Number of nodes in the network | [2, inf) |
| max_connections | Maximum number of connections a node can have | [2, num_nodes) |
| router_ratio | Percentage of routers in the network | [0.0, 1.0] |
| buffer_size | Number of packets the link layer receive buffer can hold at a time | [0, inf) |
| battery_weight | Higher the battery_weight, the more the path avoids low battery | [0.0, inf) |
| retransmission_delay | Number of seconds TCP waits before retransmission | [0.0, inf) |
| beautify | Determines whether the simulation debugs readable information or csv formatted information | [0, 1] |

## Running
```bash
ldr config.txt
```
