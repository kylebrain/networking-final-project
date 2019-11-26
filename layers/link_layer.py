from layers.layer_base import LayerBase, BaseLayerArgs
from queue import Queue

class LinkLayerArgs(BaseLayerArgs):
    pass

class LinkLayer(LayerBase):
    def transmit(self, msg):
        if self.node_data.network[self.node_data.id][msg.link.dest_id] == 0:
            raise ValueError("Link layer transmits (id = %d) can not transmit to (id = %d)" % (self.node_data.id, msg.link.dest_id))
        self.node_data.nodes[msg.link.dest_id][self.layer_id].receive_buffer.put(msg)

    def process_send(self, msg):
        if msg.link.dest_id == self.node_data.id:
            # Loop back
            self.receive_buffer.put(msg)
        else:
            self.transmit(msg)
    
    def process_receive(self, msg):
        if msg.link.dest_id == self.node_data.id:
            # Loop back
            super(LinkLayer, self).process_receive(msg)
        else:
            self.transmit(msg)
        