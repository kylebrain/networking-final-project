import unittest
import time
import load_distributed.layers as layers
import load_distributed.packet as packet
from network_factory import create_network, TIMEOUT

class TestNetworkingLayer(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stack_class_list = [layers.LinkLayer, layers.NetworkingLayer, layers.TransportLayer, layers.TestTopLayer]
        self.TEST_LAYER = len(self.stack_class_list) - 1

        BUFFER_SIZE = 100
        BATTERY_WEIGHT = 0.5
        self.RETRANSMISSION_DELAY = 1
        self.stack_args = [layers.LinkLayerArgs(BUFFER_SIZE), layers.NetworkingLayerArgs(BATTERY_WEIGHT), layers.TransportLayerArgs(self.RETRANSMISSION_DELAY), layers.TestTopLayerArgs()]

    def test_send(self):
        adjacency_matrix = [
            [0, 1],
            [1, 0]
        ]

        nodes = create_network(adjacency_matrix, self.stack_class_list, self.stack_args)

        pckt = packet.Packet()

        # Send request to node 1
        pckt.app = packet.AppPacket(0, 1, 0, 0)
        # Transport 0 is TCP
        pckt.transport = packet.TransportPacket(0)
        nodes[0][self.TEST_LAYER].send_buffer.put(pckt)
        time.sleep(TIMEOUT)

        # Transport layer has sent packet
        self.assertEqual(nodes[0][self.TEST_LAYER - 1].current_seq, 1)

        # ACK has been received and removed from ack buffer
        self.assertEqual(len(nodes[0][self.TEST_LAYER - 1].ack_buffer), 0)


if __name__ == "__main__":
    unittest.main()