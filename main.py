import layers
import time
from node_manager import NodeManager
import numpy as np
import packet

def main():
    num_nodes = 500
    max_connections = 4
    sparcity = max_connections / num_nodes
    router_ratio = 0.8
    nodeManager = NodeManager(num_nodes, sparcity, max_connections, router_ratio)
    nodes, network = nodeManager.CreateNetwork()
    print(np.matrix(network))
    app_layer_nodes = [(i, node) for i, node in enumerate(nodes) if len(node) == 4]

    for i, node in enumerate(app_layer_nodes):
        dest = app_layer_nodes[len(app_layer_nodes) - i - 1][0]
        data = node[1][3].get_data(dest)
        print("App layer (id = %d) get request found data: %s" % (node[0], data))

if __name__ == '__main__':
    main()
