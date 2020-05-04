from load_distributed.simulation_manager import SimulationManager
from load_distributed.metric_manager import MetricManager
from load_distributed.node_manager import NodeData
import load_distributed.layers as layers

def create_network(adjacency_matrix, stack_class_list, stack_args, simulation_mng = SimulationManager(), metric_mng = MetricManager()):
    nodes = []
    num_nodes = len(adjacency_matrix)
    for index in range(num_nodes):
        node_data = NodeData(index, adjacency_matrix, nodes, num_nodes)
        nodes.append(layers.create_layers(simulation_mng, metric_mng, node_data, stack_class_list, stack_args))

    return nodes