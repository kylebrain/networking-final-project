import unittest
import os

from load_distributed.node_manager import NodeManager
from load_distributed.metric_manager import MetricManager
from load_distributed.simulation_manager import SimulationManager
from load_distributed.main import netConfig


TEST_DIRECTORY = "tests/"
TEST_CONFIG = "test_config.txt"

class TestNetwork(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sim_args = netConfig(os.path.join(TEST_DIRECTORY, TEST_CONFIG))
        self.metric_manager = MetricManager()
        self.simulation_manager = SimulationManager()
        self.nodeManager = NodeManager(self.sim_args, self.metric_manager, self.simulation_manager)
        self.nodes = None
        self.network = None 


    def setUp(self):
        self.nodes, self.network = self.nodeManager.CreateNetwork()


    def test_create_num_nodes(self):
        '''
        Verifies the network is created with the correct number of nodes
        '''
        self.assertEqual(len(self.nodes), self.sim_args.num_nodes)


    def test_create_max_connections(self):
        '''
        Verifies nodes have at maximum max_connections number of connections
        '''
        for node_connections in self.network:
            connection_count = sum(connection != 0 for connection in node_connections)
            self.assertLessEqual(connection_count, self.sim_args.max_connections)


if __name__ == "__main__":
    unittest.main()