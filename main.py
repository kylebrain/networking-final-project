import layers
import time
from node_manager import NodeManager
import numpy as np

def main():
    num_nodes = 10
    nodeManager = NodeManager(num_nodes, 4 / num_nodes, 4)
    [nodes, network] = nodeManager.CreateNetwork()
    print(np.matrix(network))

    for i in range(len(nodes)):
        layer_count = len(nodes[i])
        nodes[i][layer_count - 1].send_buffer.put(i)

    for i in range(len(nodes)):
        msg = nodes[i][layer_count - 1].host_buffer.get()
        print("Top layer found: %d" % (msg, ))

if __name__ == '__main__':
    main()
