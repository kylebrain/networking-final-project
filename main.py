import layers
import time
from node_manager import NodeManager
import numpy as np

def main():
    num_nodes = 15
    max_connections = 4
    sparcity = max_connections / num_nodes
    router_ratio = 0.8
    nodeManager = NodeManager(num_nodes, sparcity, max_connections, router_ratio)
    [nodes, network] = nodeManager.CreateNetwork()
    print(np.matrix(network))

    for i in range(len(nodes)):
        layer_count = len(nodes[i])
        if layer_count == 4:
            nodes[i][layer_count - 1].send_buffer.put(i)

    for i in range(len(nodes)):
        layer_count = len(nodes[i])
        if layer_count == 4:
            msg = nodes[i][layer_count - 1].host_buffer.get()
            print("Top layer (id=%d) found: %d" % (i, msg, ))

if __name__ == '__main__':
    main()
