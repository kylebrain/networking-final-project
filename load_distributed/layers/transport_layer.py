from load_distributed.layers.layer_base import LayerBase, BaseLayerArgs
from queue import Queue
import load_distributed.packet as packet
import time
from threading import Thread

class TransportLayerArgs(BaseLayerArgs):
    def __init__(self, wait_time):
        self.wait_time = wait_time

class TransportLayer(LayerBase):
    """
    TCP provides reliable communication with acks and retransmissions
    UDP essentially acts as a passthrough layer
    """
    def __init__(self, simulation_mng, metric_mng, node_data, layer_id, args):
        super(TransportLayer, self).__init__(simulation_mng, metric_mng, node_data, layer_id, args)
        self.ack_buffer = []
        self.current_seq = 0

    def process_send(self, msg):
        """
        Add create retramission threads for all TCP packets
        """
        if msg.transport.type_id == 0 and msg.transport.tcp_type == 0:
            # When sending a TCP seq packet
            msg.transport.seq_num = self.current_seq
            self.current_seq += 1
            msg.network = packet.NetworkingPacket(self.node_data.id, msg.app.dest_id)
            retransmit_thread = Thread(target=self.retransmit, args=(msg, self.args.wait_time))
            retransmit_thread.daemon = True
            retransmit_thread.start()
            self.ack_buffer.append(packet.Packet.from_copy(msg))
        self.below_layer.send_buffer.put(msg)

    def process_receive(self, msg):
        """
        Remove packets from the ack_buffer if the ack came back for the packet's seq num
        Send an ack if a TCP packet has been received
        """
        if msg.transport.type_id == 0:
            # On TCP packet received
            if msg.transport.tcp_type == 1:
                # On ack received
                acked_message = next((seq_pckt for seq_pckt in self.ack_buffer if seq_pckt.transport.seq_num == msg.transport.ack_num), None)
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

    def retransmit(self, msg, wait_time):
        """
        Retransmit the msg after wait_time if an ack has not been received
        """
        time.sleep(wait_time)
        if msg.transport.seq_num in (pckt.transport.seq_num for pckt in self.ack_buffer):
            retransmit_thread = Thread(target=self.retransmit, args=(msg, wait_time))
            retransmit_thread.daemon = True
            retransmit_thread.start()
            self.below_layer.send_buffer.put(packet.Packet.from_copy(msg))
