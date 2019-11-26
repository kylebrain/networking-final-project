import layers
import time
from node_manager import NodeManager
import numpy as np

def main():
    num_nodes = 30
    nodeManager = NodeManager(num_nodes, 4 / num_nodes, 4)
    network = nodeManager.CreateNetwork()
    print(np.matrix(network))


    class_list = [layers.LinkLayer, layers.NetworkingLayer, layers.TransportLayer, layers.ApplicationLayer]
    args_list = [layers.LinkLayerArgs(), layers.NetworkingLayerArgs(), layers.TransportLayerArgs(), layers.ApplicationLayerArgs()]
    layer_stack = layers.create_layers(class_list, args_list)

    layer_count = len(layer_stack)

    # Add two nums for the application layer to send
    layer_stack[layer_count - 1].send_buffer.put(7)
    layer_stack[layer_count - 1].send_buffer.put(2)

    # Currently link layer places its send buffer in the receive buffer in its transmit function

    # Block get the packets out of the application layer's receive buffer
    for _ in range(2):
        msg = layer_stack[layer_count - 1].host_buffer.get()
        print("Top layer found: %d" % (msg, ))


if __name__ == '__main__':
    main()
