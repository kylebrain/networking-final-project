from layers.layer_base import LayerBase, BaseLayerArgs
from queue import Queue
from random import seed, random
import packet
import time

class ApplicationLayerArgs(BaseLayerArgs):
    pass

class ApplicationLayer(LayerBase):
    def __init__(self, simulation_mng, metric_mng, node_data, layer_id, args):
        super(ApplicationLayer, self).__init__(simulation_mng, metric_mng, node_data, layer_id, args)
        self.host_buffer = []

    def get_data(self, dest):
        pckt = packet.Packet()
        pckt.app = packet.AppPacket(self.node_data.id, dest, 0, 0)
        self.send_buffer.put(pckt)
        while not self.has_response(dest):
            pass
        return_msg = next(msg for msg in self.host_buffer)
        self.host_buffer.remove(return_msg)
        return return_msg.app.msg

    def has_response(self, dest):
        return dest in [msg.app.src_id for msg in self.host_buffer]

    def process_receive(self, msg):
        self.metric_mng.packets_received += 1
        self.metric_mng.delay.append(time.time() - msg.time_stamp)
        if msg.app.type_id == 0:
            pckt = packet.Packet()
            pckt.app = packet.AppPacket(self.node_data.id, msg.app.src_id, 1, self.create_data())
            self.send_buffer.put(pckt)
        else:
            self.host_buffer.append(msg)


    def process_send(self, msg):
        msg.transport = packet.TransportPacket(0)
        self.below_layer.send_buffer.put(msg)

    def create_data(self):
        return (9/5)*random()+32
