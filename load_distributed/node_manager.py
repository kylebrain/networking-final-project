import random
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

    def CreateNetwork(self):
        """
        Creates a network from the parameters
        Returns a list of the created nodes and an adjacency matrix of their connections
        """
        nodes = []
        added_nodes = [[0, 0]]

        node_data = NodeData(0, self.adjacency_matrix, nodes, self.num_nodes)

        # Set up common arguments for each layer
        router_args = [layers.LinkLayerArgs(self.buffer_size), layers.NetworkingLayerArgs(self.battery_weight)]
        top_layer_args = [layers.TransportLayerArgs(), layers.ApplicationLayerArgs()]

        # Set up the class lists for routers and sensors
        router_class_list = [layers.LinkLayer, layers.NetworkingLayer]
        top_layer_class_list = [layers.TransportLayer, layers.ApplicationLayer]

        sensor_args = router_args + top_layer_args
        sensor_class_list = router_class_list + top_layer_class_list

        # Create the first node which must be a sensor
        first_layer_stack = layers.create_layers(self.simulation_mng, self.metric_mng, node_data, sensor_class_list, sensor_args)
        nodes.append(first_layer_stack)

        for toAdd in range(1, self.num_nodes):
            # Gauranteed to connect to at least one node
            if len(added_nodes) == 0:
                rand_index = random.randint(0, self.num_nodes - 1)
            rand_index = random.randint(0, len(added_nodes) - 1)
            added_nodes[rand_index][1] += 1
            neighbor = added_nodes[rand_index][0]
            if added_nodes[rand_index][1] >= self.max_connections:
                del added_nodes[rand_index]
            self.adjacency_matrix[toAdd][neighbor] = 1
            self.adjacency_matrix[neighbor][toAdd] = 1
            added_nodes.append([toAdd, 1])

            node_data = NodeData(toAdd, self.adjacency_matrix, nodes, self.num_nodes)

            # Chance to be a router or sensor application
            if random.random() < self.router_ratio:
                layer_stack = layers.create_layers(self.simulation_mng, self.metric_mng, node_data, router_class_list, router_args)
                nodes.append(layer_stack)
            else:
                layer_stack = layers.create_layers(self.simulation_mng, self.metric_mng, node_data, sensor_class_list, sensor_args)
                nodes.append(layer_stack)

            # Try to connect to other nodes with some probability
            toAdd_index = self.num_nodes
            for i in range(len(added_nodes)):
                if toAdd == added_nodes[i][0]:
                    toAdd_index = i
            otherNode_index = 0
            length = len(added_nodes)
            while otherNode_index < length:
                if random.random() < self.sparcity:
                    if otherNode_index == toAdd_index or self.adjacency_matrix[toAdd][added_nodes[otherNode_index][0]] != 0:
                        otherNode_index += 1
                        continue
                    added_nodes[otherNode_index][1] += 1
                    added_nodes[toAdd_index][1] += 1
                    neighbor = added_nodes[otherNode_index][0]
                    if added_nodes[otherNode_index][1] >= self.max_connections:
                        if added_nodes[toAdd_index][1] >= self.max_connections:
                            added_nodes[otherNode_index][1] -= 1
                            added_nodes[toAdd_index][1] -= 1
                            otherNode_index += 1
                            continue
                        del added_nodes[otherNode_index]
                        if otherNode_index < toAdd_index:
                            toAdd_index -= 1
                        otherNode_index -= 1
                    if added_nodes[toAdd_index][1] >= self.max_connections:
                        del added_nodes[toAdd_index]
                        otherNode_index = self.num_nodes
                    self.adjacency_matrix[toAdd][neighbor] = 1
                    self.adjacency_matrix[neighbor][toAdd] = 1
                otherNode_index += 1
                length = len(added_nodes)
        return nodes, self.adjacency_matrix
