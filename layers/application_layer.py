from layers.layer_base import LayerBase, BaseLayerArgs
from queue import Queue
from random import seed, random

class ApplicationLayerArgs(BaseLayerArgs):
    pass

class ApplicationLayer(LayerBase):
    def __init__(self, node_data, layer_id, args):
        super(ApplicationLayer, self).__init__(node_data, layer_id, args)
        self.host_buffer = Queue()
		self.msg_type = 0	# 0 - send, 1 - ack... Assume every application starts at send


    def process_receive(self, msg):
        print("Node has battery: %f" % (self.node_data.battery,))
		self.check_type(msg)
        self.host_buffer.put(msg)

    def process_send(self, msg):
        super(ApplicationLayer, self).process_send(ApplicationPacket( self.msg_type, self.create_data().msg_type))

    def create_data(self):
        seed(1)
        if self.msg_type == 0:
            return (9/5)*random()+32	# returns some random Fahrenheit value for DATA
        else:
            return 1	# sample num used for ACK

    def print_data(self):
        print(self.host_buffer.get())

    def check_type(self, msg):
	    self.msg_type = msg.get_type

