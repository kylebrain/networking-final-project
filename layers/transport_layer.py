from layers.layer_base import LayerBase, BaseLayerArgs
from queue import Queue
import packet

class TransportLayerArgs(BaseLayerArgs):
    pass

class TransportLayer(LayerBase):
    def __init__(self, node_data, layer_id, args):
        super(TransportLayer, self).__init__(node_data, layer_id, args)
        self.ack_buffer = []
        self.current_seq = 0

    def process_send(self, msg):
        if msg.transport.type_id == 0 and msg.transport.tcp_type == 0:
            # When sending a TCP seq packet
            msg.transport.seq_num = self.current_seq
            self.current_seq += 1
            msg.network = packet.NetworkingPacket(self.node_data.id, msg.app.dest_id)
            self.ack_buffer.append(msg)  # might need to use copy constructor
        self.below_layer.send_buffer.put(msg)

    def process_receive(self, msg):
        if msg.transport.type_id == 0:
            # On TCP packet received
            if msg.transport.tcp_type == 1:
                # On ack received
                acked_message = next(seq_pckt for seq_pckt in self.ack_buffer if seq_pckt.transport.seq_num == msg.transport.ack_num)
                if acked_message is not None:
                    self.ack_buffer.remove(acked_message)
            else:
                # On packet received
                pckt = packet.Packet()
                pckt.transport = packet.TransportPacket(0, 1, 0, msg.transport.seq_num)
                pckt.network = packet.NetworkingPacket(self.node_data.id, msg.network.src_id)
                self.send_buffer.put(pckt)
                self.above_layer.receive_buffer.put(msg)
        else:
            # On UDP packet received
            self.above_layer.receive_buffer.put(msg)


