import unittest
import time
import load_distributed.layers as layers
import load_distributed.packet as packet
from network_factory import create_network, TIMEOUT

class TestApplicationLayer(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stack_class_list = [layers.LinkLayer, layers.NetworkingLayer, layers.TransportLayer, layers.ApplicationLayer]
        self.TEST_LAYER = len(self.stack_class_list) - 1

        BUFFER_SIZE = 100
        BATTERY_WEIGHT = 0.5
        self.RETRANSMISSION_DELAY = 1
        self.stack_args = [layers.LinkLayerArgs(BUFFER_SIZE), layers.NetworkingLayerArgs(BATTERY_WEIGHT), layers.TransportLayerArgs(self.RETRANSMISSION_DELAY), layers.ApplicationLayerArgs()]


    def test_send(self):
        adjacency_matrix = [
            [0, 1],
            [1, 0]
        ]

        nodes = create_network(adjacency_matrix, self.stack_class_list, self.stack_args)

        data = nodes[0][self.TEST_LAYER].get_data(1, timeout=TIMEOUT)
        self.assertIsNotNone(data, "Application did not respond with data")


if __name__ == "__main__":
    unittest.main()
