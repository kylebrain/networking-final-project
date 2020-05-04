import unittest
import time
import load_distributed.layers as layers
import load_distributed.packet as packet
from network_factory import create_network, TIMEOUT

class TestLinkLayer(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stack_class_list = [layers.LinkLayer, layers.TestTopLayer]
        self.TEST_LAYER = len(self.stack_class_list) - 1

        BUFFER_SIZE = 100
        self.stack_args = [layers.LinkLayerArgs(BUFFER_SIZE), layers.TestTopLayerArgs()]


    def test_send(self):
        adjacency_matrix = [
            [0, 1],
            [1, 0]
        ]

        nodes = create_network(adjacency_matrix, self.stack_class_list, self.stack_args)

        pckt = packet.Packet()
        pckt.link = packet.LinkPacket(0, 1)
        nodes[0][self.TEST_LAYER].send_buffer.put(pckt)

        resp = nodes[1][self.TEST_LAYER].get_response(timeout=TIMEOUT)
        self.assertEqual(resp, pckt, "Link layer was not able to send packet")


    def test_send_no_connection(self):
        adjacency_matrix = [
            [0, 0],
            [0, 0]
        ]

        nodes = create_network(adjacency_matrix, self.stack_class_list, self.stack_args)

        pckt = packet.Packet()
        pckt.link = packet.LinkPacket(0, 1)

        nodes[0][self.TEST_LAYER].send_buffer.put(pckt)

        resp = nodes[1][self.TEST_LAYER].get_response(timeout=TIMEOUT)
        self.assertIsNone(resp, "Link layer was able to send across a disconnected link")


if __name__ == "__main__":
    unittest.main()
