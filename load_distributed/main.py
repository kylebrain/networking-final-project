import load_distributed.layers
import time
from load_distributed.node_manager import NodeManager
from load_distributed.metric_manager import MetricManager
from load_distributed.simulation_manager import SimulationManager
import numpy as np
import load_distributed.packet
import sys
import fileinput
import re
import time
import random
from threading import Thread

def main():
    if len(sys.argv) < 2:
        print ("Improper running. (EX: ldr config.txt)")
        return

    # Create the simulation arguments from the config file
    sim_args = netConfig(sys.argv[1])

    # Create the managers
    metric_manager = MetricManager()
    simulation_manager = SimulationManager()
    nodeManager = NodeManager(sim_args, metric_manager, simulation_manager)

    # Create the network
    nodes, _ = nodeManager.CreateNetwork()

    # Get all of the application layer (sensors) IDs
    app_layer_nodes = [i for i, node in enumerate(nodes) if len(node) == 4]

    if sim_args.beautify:
        print("Simulation Running", flush=True)
        print(sim_args.__dict__, flush=True)

    start_time = time.time()
    request_period = 0.01

    # Every request_period seconds, select a random sensor node to make a data request from a random sensor node
    while simulation_manager.sim_running:
        src_id, dest_id = get_src_dest(app_layer_nodes)
        req_thread = Thread(target=make_request, args=(nodes, src_id, dest_id, sim_args.beautify))
        req_thread.daemon = True
        req_thread.start()
        time.sleep(request_period)

    time_alive = time.time() - start_time

    # Print out simulation metrics
    if sim_args.beautify:
        print("Battery dead. Quiting Simulation!")
        print("Percent loss: %f" % (float(metric_manager.total_loss) / metric_manager.total_packets, ))
        print("Application packets received: %d" % (metric_manager.packets_received, ))
        print("Average delay: %f" % (np.mean(metric_manager.delay), ))
        print("Time alive: %f" % (time_alive))
    else:
        print("%f,%f,%d,%f,%f" %
             (sim_args.battery_weight,
             float(metric_manager.total_loss) / metric_manager.total_packets,
             metric_manager.packets_received,
             np.mean(metric_manager.delay),
             time_alive))

def get_src_dest(app_layer_nodes):
    """
    Returns a pair of distinct random nodes
    """
    src_id = random.choice(app_layer_nodes)
    dest_id = random.choice(app_layer_nodes)
    while dest_id == src_id:
        dest_id = random.choice(app_layer_nodes)

    return src_id , dest_id


def make_request(nodes, src, dest, beautify):
    """
    Make the src request data from the dest
    """
    data = nodes[src][3].get_data(dest)
    if beautify:
        print("App layer (id = %d) get request found data: %.3f from node (id = %d)" % (src, data, dest), flush=True)

class SimulationArgs():
    """
    Includes arguments to be changed by the config file
    num_nodes - number of nodes in the network
    sparcity - number from [0, 1] which represents the density of connections in the network
    max_connections - maximum number of connections a node can have
    router_ratio - percentage of routers in the network
    buffer_size - number of packets the link layer receive buffer can hold at a time
    battery_weight - higher the battery_weight, the more the path avoids low battery
    retransmission_delay - number of seconds TCP waits before retransmission
    beautify - determines whether the simulation debugs readable information or csv formatted information
    """
    def __init__(self):
        self.num_nodes = 0
        self.sparcity = 0.0
        self.max_connections = 0
        self.router_ratio = 0.0
        self.buffer_size = 0
        self.battery_weight = 0.0
        self.retransmission_delay = 0.0
        self.beautify = False

def netConfig(path):
    """
    Read the config file from the specified path
    Returns - Populated SimulationArgs object with data from the config file
    """
    ret = SimulationArgs()
    with open(path, 'r') as fp:
        info = fp.readlines()
        for i in info:
            if "num_nodes" in i:
                d = re.findall(r"\d+", i)
                ret.num_nodes = int(d[0])
            elif "max_connections" in i:
                d = re.findall(r"\d+", i)
                ret.max_connections = int(d[0])
            elif "router_ratio" in i:
                d = re.findall(r"\d+\.\d+", i)
                ret.router_ratio = float(d[0])
            elif "buffer_size" in i:
                d = re.findall(r"\d+", i)
                ret.buffer_size = int(d[0])
            elif "battery_weight" in i:
                d = re.findall(r"\d+\.\d+", i)
                ret.battery_weight = float(d[0])
            elif "retransmission_delay" in i:
                d = re.findall(r"\d+\.\d+", i)
                ret.retransmission_delay = float(d[0])
            elif "beautify" in i:
                d = re.findall(r"\d+", i)
                ret.beautify = bool(int(d[0]))
    ret.sparcity = float(ret.max_connections) / ret.num_nodes
    return ret

if __name__ == '__main__':
    main()
