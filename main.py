import layers
import time
from node_manager import NodeManager
from metric_manager import MetricManager
import numpy as np
import packet
import sys
import fileinput
import re
import time
import random
from threading import Thread

def main():
    if len(sys.argv) < 2:
        print ("Improper running. (EX: python3 main.py config.txt)")
        return
    sim_args = netConfig(sys.argv[1])

    metric_manager = MetricManager()
    nodeManager = NodeManager(sim_args, metric_manager)
    nodes, network = nodeManager.CreateNetwork()
    print(np.matrix(network))
    app_layer_nodes = [i for i, node in enumerate(nodes) if len(node) == 4]

    print(app_layer_nodes)

    sim_run_time = 20
    start_time = time.time()
    request_period = 0.1
    while time.time() - start_time < sim_run_time:
        src_id, dest_id = get_src_dest(app_layer_nodes)
        req_thread = Thread(target=make_request, args=(nodes, src_id, dest_id))
        req_thread.daemon = True
        req_thread.start()
        time.sleep(request_period)

    print("Total loss: %d" % (metric_manager.total_loss, ))
    print("Packets received: %d" % (metric_manager.packets_received, ))
    print("Average delay: %f" % (np.mean(metric_manager.delay), ))

def get_src_dest(app_layer_nodes):
    src_id = random.choice(app_layer_nodes)
    dest_id = random.choice(app_layer_nodes)
    while dest_id == src_id:
        dest_id = random.choice(app_layer_nodes)

    return src_id , dest_id


def make_request(nodes, src, dest):
    data = nodes[src][3].get_data(dest)
    print("App layer (id = %d) get request found data: %s from node (id = %d)" % (src, data, dest))

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
