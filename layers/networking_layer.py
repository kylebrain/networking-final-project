from layers.layer_base import LayerBase, BaseLayerArgs
from queue import Queue
from packet import LinkPacket, NetworkingPacket, Packet
from threading import Thread
import time
from djikstra import djikstra

class NetworkingLayerArgs(BaseLayerArgs):
    pass

class NetworkingLayer(LayerBase):
    def __init__(self, node_data, layer_id, args):
        super(NetworkingLayer, self).__init__(node_data, layer_id, args)

        self.previous_dist_vect = []
        dist_vect_thread = Thread(target=self.periodic_distance_vector)
        dist_vect_thread.daemon = True
        #dist_vect_thread.start()

    def process_send(self, msg):
        if msg.network.dest_id == self.node_data.id:
            # Loopback
            self.receive_buffer.put(msg)
        elif msg.network.dest_id == -1:
            ignore_list = [msg.network.src_id, ]
            if msg.link is not None:
                ignore_list.append(msg.link.src_id)
            self.broadcast(msg, ignore_list)
        else:
            #dest = next(i for i, x in enumerate(self.node_data.network[self.node_data.id]) if x == 1 and i != self.node_data.id)
            path = djikstra(self.node_data.id, msg.network.dest_id, self.node_data.network, self.node_data.battery_table)
            dest = path[1]
            #if msg.link is not None and dest == msg.link.src_id:
            #    print("Loop detected between link (id=%d) and (id=%d)" % (self.node_data.id, dest))
            #    return
            msg.link = LinkPacket(self.node_data.id, dest)
            super(NetworkingLayer, self).process_send(msg)

    def process_receive(self, msg):
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

    def periodic_distance_vector(self):
        while True:
            self.broadcast_distance_vector()
            time.sleep(0.5)

    def broadcast_distance_vector(self):
        time.sleep(1)
        msg = Packet()
        # Add the distance vector to the payload
        msg.payload = (self.node_data.id, self.node_data.battery)
        msg.type = 1
        msg.time_stamp = time.time()
        msg.network = NetworkingPacket(self.node_data.id, -1)
        self.send_buffer.put(msg)

    def broadcast(self, msg, ignore = []):
        for i, link in enumerate(self.node_data.network[self.node_data.id]):
            if link > 0 and i != self.node_data.id and i not in ignore:

                # create copy constructor
                cur_msg = Packet()
                cur_msg.payload = msg.payload
                cur_msg.type = msg.type
                cur_msg.network = msg.network
                cur_msg.time_stamp = msg.time_stamp

                cur_msg.link = LinkPacket(self.node_data.id, i)
                self.below_layer.send_buffer.put(cur_msg)
