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
        self.nodeManager = None


    def setUp(self):
        self.nodeManager = NodeManager(self.sim_args, self.metric_manager, self.simulation_manager)


    def test_create_network(self):
        # Create the network
        nodes, _ = self.nodeManager.CreateNetwork()

        self.assertEqual(len(nodes), self.sim_args.num_nodes)


if __name__ == "__main__":
    unittest.main()