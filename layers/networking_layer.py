from layers.layer_base import LayerBase, BaseLayerArgs
from queue import Queue
from packet import LinkPacket

class NetworkingLayerArgs(BaseLayerArgs):
    pass

class NetworkingLayer(LayerBase):
    def process_send(self, msg):
        if msg.network.dest_id == self.node_data.id:
            # Loopback
            self.receive_buffer.put(msg)
        else:
            dest = next(i for i, x in enumerate(self.node_data.network[self.node_data.id]) if x == 1 and i != self.node_data.id)

            if msg.link is not None and dest == msg.link.src_id:
                print("Loop detected between link (id=%d) and (id=%d)" % (self.node_data.id, dest))
                return
            msg.link = LinkPacket(self.node_data.id, dest)
            super(NetworkingLayer, self).process_send(msg)

    def process_receive(self, msg):
        if msg.network.dest_id == self.node_data.id:
            super(NetworkingLayer, self).process_receive(msg)
        else:
            self.send_buffer.put(msg)