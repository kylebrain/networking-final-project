from load_distributed.layers.layer_base import LayerBase, BaseLayerArgs
from queue import Queue
import sys

class LinkLayerArgs(BaseLayerArgs):
    def __init__(self, buffer_size):
        self.buffer_size = buffer_size

class LinkLayer(LayerBase):
    """
    Transmits packets across links
    """
    def transmit(self, msg):
        """
        Transmits a link layer packet to its destination only if:
            A link exists between the two packet
            The destination's receive buffer is not full
        Decreases from the battery life
            Broadcast control battery packets subtract less as they are consider smaller
            Ends the simulation if the battery goes below 0
            After the battery drops a given amount, broadcast the battery life to the network
        """
        # Do not transmit if the simulation is not running
        if not self.simulation_mng.sim_running:
            return

        # Throw an error if trying to transmit across a link that does not exist
        if self.node_data.network[self.node_data.id][msg.link.dest_id] == 0:
            raise ValueError("Link layer transmits (id = %d) can not transmit to (id = %d)" % (self.node_data.id, msg.link.dest_id))

        self.metric_mng.total_packets += 1

        # Only transmit if the receiving buffer is not full
        if self.node_data.nodes[msg.link.dest_id][self.layer_id].receive_buffer.qsize() < self.args.buffer_size:
            self.node_data.nodes[msg.link.dest_id][self.layer_id].receive_buffer.put(msg)
        else:
            self.metric_mng.total_loss += 1

        # Subtract from the battery life
        if self.node_data.battery > 0:
            prevBattery = self.node_data.battery
            if msg.app is None:
                self.node_data.battery -= 5
            else:
                self.node_data.battery -= 10
            if self.node_data.battery <= 0:
                self.simulation_mng.sim_running = False
            else:
                for i in range(20):
                    if prevBattery > i * 500 and self.node_data.battery <= i * 500:
                        self.above_layer.broadcast_distance_vector()

    def process_send(self, msg):
        if msg.link.dest_id == self.node_data.id:
            # Loop back
            self.receive_buffer.put(msg)
        else:
            self.transmit(msg)

    def process_receive(self, msg):
        """
        Throws an error if the node receives a message not intended for itself
        """
        if msg.link.dest_id != self.node_data.id:
            raise ValueError("Link layer (id = %d) received data intended for (id = %d)" % (self.node_data.id, msg.link.dest_id))
        super(LinkLayer, self).process_receive(msg)
