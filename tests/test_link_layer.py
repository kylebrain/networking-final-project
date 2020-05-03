import unittest
from load_distributed.simulation_manager import SimulationManager
from load_distributed.metric_manager import MetricManager
from load_distributed.node_manager import NodeData
import load_distributed.layers as layers
import load_distributed.packet as packet

class TestLinkLayer(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nodes = []

    def setUp(self):
        BUFFER_SIZE = 100
        NUM_NODES = 2
        simulation_mng = SimulationManager()
        metric_mng = MetricManager()
        adjacency_matrix = [
            [1, 1],
            [1, 1]
        ]
        stack_class_list = [layers.LinkLayer, layers.TestTopLayer]
        stack_args = [layers.LinkLayerArgs(BUFFER_SIZE), layers.TestTopLayerArgs()]

        node_data = NodeData(0, adjacency_matrix, self.nodes, NUM_NODES)
        self.nodes.append(layers.create_layers(simulation_mng, metric_mng, node_data, stack_class_list, stack_args))
        node_data = NodeData(1, adjacency_matrix, self.nodes, NUM_NODES)
        self.nodes.append(layers.create_layers(simulation_mng, metric_mng, node_data, stack_class_list, stack_args))


    def test_send(self):
        pckt = packet.Packet()
        pckt.link = packet.LinkPacket(0, 1)
        self.nodes[0][1].send_buffer.put(pckt)

        resp = self.nodes[1][1].get_response()
        self.assertEqual(resp, pckt)