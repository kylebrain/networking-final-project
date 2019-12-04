from layers.layer_base import LayerBase, BaseLayerArgs
from queue import Queue
import sys

class LinkLayerArgs(BaseLayerArgs):
    def __init__(self, buffer_size):
        self.buffer_size = buffer_size

class LinkLayer(LayerBase):
    def transmit(self, msg):
        if not self.simulation_mng.sim_running:
            return
        if self.node_data.network[self.node_data.id][msg.link.dest_id] == 0:
            print(msg)
            raise ValueError("Link layer transmits (id = %d) can not transmit to (id = %d)" % (self.node_data.id, msg.link.dest_id))

        if self.node_data.nodes[msg.link.dest_id][self.layer_id].receive_buffer.qsize() < self.args.buffer_size:
            self.node_data.nodes[msg.link.dest_id][self.layer_id].receive_buffer.put(msg)
        else:
            self.metric_mng.total_loss += 1

        if self.node_data.battery > 0:
            self.node_data.battery -= 1
            if self.node_data.battery <= 0:
                self.simulation_mng.sim_running = False
                print("Link layer (id=%d) dead, battery table: %s" % (self.node_data.id, self.node_data.battery_table))
                #sys.exit(0)

    def process_send(self, msg):
        if msg.link is None:
            print(msg)
        if msg.link.dest_id == self.node_data.id:
            # Loop back
            self.receive_buffer.put(msg)
        else:
            self.transmit(msg)

    def process_receive(self, msg):
        if msg.link.dest_id != self.node_data.id:
            raise ValueError("Link layer (id = %d) received data intended for (id = %d)" % (self.node_data.id, msg.link.dest_id))
        super(LinkLayer, self).process_receive(msg)
