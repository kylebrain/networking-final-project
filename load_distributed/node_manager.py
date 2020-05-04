import random
import functools
import load_distributed.layers as layers

class NodeData():
    def __init__(self, id, network, nodes, numNodes):
        self.id = id
        self.battery = 10000
        self.battery_table = [-1]*numNodes
        self.network = network
        self.nodes = nodes


class NodeManager():
    """
    Creates a random network of nodes
    """
    def __init__(self, sim_args, metric_mng, simulation_mng):
        self.num_nodes = sim_args.num_nodes
        self.sparcity = sim_args.sparcity
        self.router_ratio = sim_args.router_ratio
        self.max_connections = sim_args.max_connections
        self.buffer_size = sim_args.buffer_size
        self.battery_weight = sim_args.battery_weight
        self.metric_mng = metric_mng
        self.simulation_mng = simulation_mng
        self.adjacency_matrix = [[0 for i in range(sim_args.num_nodes)] for j in range(sim_args.num_nodes)]

        # Set up common arguments for each layer
        self.ROUTER_ARGS = [layers.LinkLayerArgs(self.buffer_size), layers.NetworkingLayerArgs(self.battery_weight)]
        top_layer_args = [layers.TransportLayerArgs(sim_args.retransmission_delay), layers.ApplicationLayerArgs()]

        # Set up the class lists for routers and sensors
        self.ROUTER_CLASS_LIST = [layers.LinkLayer, layers.NetworkingLayer]
        top_layer_class_list = [layers.TransportLayer, layers.ApplicationLayer]

        self.SENSOR_ARGS = self.ROUTER_ARGS + top_layer_args
        self.SENSOR_CLASS_LIST = self.ROUTER_CLASS_LIST + top_layer_class_list


    def make_connection(self, src, dest):
        self.adjacency_matrix[src][dest] = 1
        self.adjacency_matrix[dest][src] = 1


    def is_connected(self, src, dest):
        return self.adjacency_matrix[src][dest] != 0


    def get_random_connection(self, added_nodes, src=None):
        return random.choice(list(self.get_potential_connections(added_nodes, src).keys()))


    def get_potential_connections(self, added_nodes, src=None):
        return {index: connections for index, connections in enumerate(added_nodes) if connections < self.max_connections and (src is None or src != index)}


    def add_random_connections(self, added_nodes, src):
        potential_connections = self.get_potential_connections(added_nodes, src)

        if len(potential_connections) == 0:
            raise ValueError("node_manager add_random_connections cannot add connection if there are no valid connection open to be made")

        for node, connections in potential_connections.items():
            # Make connection if not already connected and random selection
            if not self.is_connected(src, node) and random.random() < self.sparcity:

                double_deletion = connections == self.max_connections - 1 and added_nodes[src] == self.max_connections - 1
                connections_empty = False
                # If making this connection would max both nodes, make sure there are more than 2 nodes
                if double_deletion:
                    connections_empty = len(self.get_potential_connections(added_nodes, src)) == 1

                if not connections_empty:
                    self.make_connection(src, node)
                    added_nodes[src] += 1
                    added_nodes[node] += 1

                    if added_nodes[src] >= self.max_connections:
                        # Stop if the src node cannot make more connections
                        break


    def add_node(self, toAdd, nodes, added_nodes, create_router, create_sensor):
        # Make one connection to existing nodes
        rand_index = self.get_random_connection(added_nodes)
        added_nodes[rand_index] += 1
        self.make_connection(toAdd, rand_index)

        # Add the current node with one connection
        added_nodes.append(1)

        # Randomly create a sensor or router node
        new_node = self.create_sensor_or_router(toAdd, create_router, create_sensor)
        nodes.append(new_node)

        # Add random connections to other nodes
        self.add_random_connections(added_nodes, toAdd)


    def create_node(self, node_id, nodes, stack_class_list, stack_args):
        node_data = NodeData(node_id, self.adjacency_matrix, nodes, self.num_nodes)
        return layers.create_layers(self.simulation_mng, self.metric_mng, node_data, stack_class_list, stack_args)


    def create_node_closure(self, nodes, stack_class_list, stack_args):
        return functools.partial(self.create_node, nodes=nodes, stack_class_list=stack_class_list, stack_args=stack_args)


    def create_sensor_or_router(self, node_id, create_router, create_sensor):
        if random.random() < self.router_ratio:
            return create_router(node_id)
        else:
            return create_sensor(node_id)


    def get_router_sensor_factories(self,
                                    nodes,
                                    router_class_list=None,
                                    router_args=None,
                                    sensor_class_list=None,
                                    sensor_args=None):
        if router_class_list is None:
            router_class_list = self.ROUTER_CLASS_LIST
        if router_args is None:
            router_args = self.ROUTER_ARGS
        if sensor_class_list is None:
            sensor_class_list = self.SENSOR_CLASS_LIST
        if sensor_args is None:
            sensor_args = self.SENSOR_ARGS
        return self.create_node_closure(nodes, router_class_list, router_args),\
               self.create_node_closure(nodes, sensor_class_list, sensor_args)


    def CreateNetwork(self):
        """
        Creates a network from the parameters
        Returns a list of the created nodes and an adjacency matrix of their connections
        """
        nodes = []
        added_nodes = []

        create_router, create_sensor = self.get_router_sensor_factories(nodes)

        # Create the first node which must be a sensor
        first_layer_stack = create_sensor(0)
        nodes.append(first_layer_stack)
        added_nodes.append(0)

        for toAdd in range(1, self.num_nodes):
            self.add_node(toAdd, nodes, added_nodes, create_router, create_sensor)

        return nodes, self.adjacency_matrix
