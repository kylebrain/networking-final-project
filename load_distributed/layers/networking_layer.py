from load_distributed.layers.layer_base import LayerBase, BaseLayerArgs
from queue import Queue
from load_distributed.packet import LinkPacket, NetworkingPacket, Packet
from threading import Thread
from load_distributed.djikstra import djikstra
import time
import random

class NetworkingLayerArgs(BaseLayerArgs):
    def __init__(self, battery_weight):
        self.battery_weight = battery_weight

class NetworkingLayer(LayerBase):
    """
    Routes or broadcasts packets
    """
    def __init__(self, simulation_mng, metric_mng, node_data, layer_id, args):
        super(NetworkingLayer, self).__init__(simulation_mng, metric_mng, node_data, layer_id, args)

        self.previous_dist_vect = []
        self.numSent = 0

    def process_send(self, msg):
        """
        Loopback if the destination is itself
        Broadcast if the destination is -1
            Do not broadcast to the node that the packet was received from
        Use Distributed Load Routing otherwise to route the packet
        """
        if msg.network.dest_id == self.node_data.id:
            # Loopback
            self.receive_buffer.put(msg)
        elif msg.network.dest_id == -1:
            ignore_list = [msg.network.src_id, ]
            if msg.link is not None:
                ignore_list.append(msg.link.src_id)
            self.broadcast(msg, ignore_list)
        else:
            path = djikstra(self.node_data.id, msg.network.dest_id, self.node_data.network, self.node_data.battery_table, self.args.battery_weight)
            if len(path) == 0:
                raise RuntimeError("Networking layer could not find a path to the destination")
            dest = path[1]
            msg.link = LinkPacket(self.node_data.id, dest)
            super(NetworkingLayer, self).process_send(msg)

    def process_receive(self, msg):
        """
        If receiving a battery broadcast, add the data to the node's battery table
        If the message is intended for the node, forward it up to the transport layer
        If the message is not intended for itself, place in the send buffer
        """
        if msg.type == 1:
            msg_sig = (msg.network.src_id, msg.time_stamp)
            if msg_sig not in self.previous_dist_vect:
                self.node_data.battery_table[msg.payload[0]] = msg.payload[1]
                self.previous_dist_vect.append(msg_sig)
                if msg.network.dest_id == -1:
                    self.send_buffer.put(msg)
        elif msg.network.dest_id == self.node_data.id:
            super(NetworkingLayer, self).process_receive(msg)
        else:
            self.send_buffer.put(msg)

    def broadcast_distance_vector(self):
        """
        Create a broadcast packet containing the node's ID and current battery life
        """
        msg = Packet()
        # Add the distance vector to the payload
        msg.payload = (self.node_data.id, self.node_data.battery)
        msg.type = 1
        msg.network = NetworkingPacket(self.node_data.id, -1)
        self.send_buffer.put(msg)

    def broadcast(self, msg, ignore = []):
        """
        Broadcast to every neighboring node except for those specified in the ignore list
        """
        for i, link in enumerate(self.node_data.network[self.node_data.id]):
            if link > 0 and i != self.node_data.id and i not in ignore:

                # create copy constructor
                cur_msg = Packet.from_copy(msg)

                cur_msg.link = LinkPacket(self.node_data.id, i)
                self.below_layer.send_buffer.put(cur_msg)
