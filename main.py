import layers
import time
from node_manager import NodeManager
import numpy as np
import packet

def main():
    num_nodes = 15
    max_connections = 4
    sparcity = max_connections / num_nodes
    router_ratio = 0.8
    nodeManager = NodeManager(num_nodes, sparcity, max_connections, router_ratio)
    nodes, network = nodeManager.CreateNetwork()
    print(np.matrix(network))
    app_layer_nodes = [(i, node) for i, node in enumerate(nodes) if len(node) == 4]

    for i, node in enumerate(app_layer_nodes):
        cur_packet = packet.Packet()
        cur_packet.network = packet.NetworkingPacket(node[0], app_layer_nodes[len(app_layer_nodes) - i - 1][0])
        node[1][3].send_buffer.put(cur_packet)

    for i in range(len(nodes)):
        layer_count = len(nodes[i])
        if layer_count == 4:
            msg = nodes[i][layer_count - 1].host_buffer.get()
            print("Top layer (id=%d) found: %s" % (i, msg, ))

if __name__ == '__main__':
    main()
