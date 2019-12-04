import layers
import time
from node_manager import NodeManager
from metric_manager import MetricManager
import numpy as np
import packet
import sys
import fileinput
import re

def main():
    if len(sys.argv) < 2:
        print ("Improper running. (EX: python3 main.py config.txt)")
        return
    sim_args = netConfig(sys.argv[1])

    metric_manager = MetricManager()
    nodeManager = NodeManager(sim_args, metric_manager)
    nodes, network = nodeManager.CreateNetwork()
    print(np.matrix(network))
    app_layer_nodes = [(i, node) for i, node in enumerate(nodes) if len(node) == 4]

    for i, node in enumerate(app_layer_nodes):
        dest = app_layer_nodes[len(app_layer_nodes) - i - 1][0]
        data = node[1][3].get_data(dest)
        print("App layer (id = %d) get request found data: %s" % (node[0], data))

    print("Total loss: %d" % (metric_manager.total_loss, ))
    print("Packets received: %d" % (metric_manager.packets_received, ))
    print("Average delay: %f" % (np.mean(metric_manager.delay), ))

class SimulationArgs():
    def __init__(self):
        self.num_nodes = 0
        self.sparcity = 0.0
        self.max_connections = 0
        self.router_ratio = 0.0
        self.buffer_size = 0
        self.battery_weight = 0.0

def netConfig(path):
    ret = SimulationArgs()
    with open(path, 'r') as fp:
        info = fp.readlines()
        for i in info:
            if "num_nodes" in i:
                d = re.findall("\d+", i)
                ret.num_nodes = int(d[0])
            elif "max_connections" in i:
                d = re.findall("\d+", i)
                ret.max_connections = int(d[0])
            elif "router_ratio" in i:
                d = re.findall("\d+\.\d+", i)
                ret.router_ratio = float(d[0])
            elif "buffer_size" in i:
                d = re.findall("\d+", i)
                ret.buffer_size = int(d[0])
            elif "battery_weight" in i:
                d = re.findall("\d+\.\d+", i)
                ret.battery_weight = float(d[0])
    ret.sparcity = float(ret.max_connections) / ret.num_nodes
    return ret

if __name__ == '__main__':
    main()
