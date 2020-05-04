from load_distributed.layers.layer_base import LayerBase, BaseLayerArgs
from queue import Queue
from random import seed, random
import load_distributed.packet as packet
import time

class ApplicationLayerArgs(BaseLayerArgs):
    pass

class ApplicationLayer(LayerBase):
    """
    Allows the user to make request for data from other sensor nodes in the network
    """
    def __init__(self, simulation_mng, metric_mng, node_data, layer_id, args):
        super(ApplicationLayer, self).__init__(simulation_mng, metric_mng, node_data, layer_id, args)
        self.host_buffer = []

    def get_data(self, dest, timeout=None):
        """
        Sends a data request to the dest node
        Waits until a response is received from the dest node
        """
        pckt = packet.Packet()
        pckt.app = packet.AppPacket(self.node_data.id, dest, 0, 0)
        self.send_buffer.put(pckt)

        start = time.time()
        while not self.has_response(dest):
            if timeout is not None and time.time() >= start + timeout:
                return None

        return_msg = next(msg for msg in self.host_buffer)
        self.host_buffer.remove(return_msg)
        return return_msg.app.msg

    def has_response(self, dest):
        """
        Returns true if a response has been received from the dest node
        """
        return dest in [msg.app.src_id for msg in self.host_buffer]

    def process_receive(self, msg):
        """
        If a request is received, it create a response and sends it
        If a response is received, it places it in the host_buffer to be used by the get_data function
        """
        self.metric_mng.packets_received += 1
        self.metric_mng.delay.append(time.time() - msg.time_stamp)
        if msg.app.type_id == 0:
            pckt = packet.Packet()
            pckt.app = packet.AppPacket(self.node_data.id, msg.app.src_id, 1, self.create_data())
            self.send_buffer.put(pckt)
        else:
            self.host_buffer.append(msg)


    def process_send(self, msg):
        """
        Create a TCP header to be forwared to the transport layer
        """
        msg.transport = packet.TransportPacket(0)
        self.below_layer.send_buffer.put(msg)

    def create_data(self):
        """
        Returns a random number [0, 20) to simulate a sensor reading
        """
        return random() * 20
