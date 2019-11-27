from layers.layer_base import LayerBase, BaseLayerArgs
from queue import Queue
from random import seed, random

class ApplicationLayerArgs(BaseLayerArgs):
    pass

class ApplicationLayer(LayerBase):
    def __init__(self, node_data, layer_id, args):
        super(ApplicationLayer, self).__init__(node_data, layer_id, args)
        self.host_buffer = Queue()


    def process_receive(self, msg):
        print("Node has battery: %f" % (self.node_data.battery,))
        self.host_buffer.put(msg)

    def process_send(self, msg):
        super(ApplicationLayer, self).process_send(self.create_data())

    def create_data(self):
            seed(1)
            return (9/5)*random()+32	# returns some random Fahrenheit value for data

    def print_data(self):
            print(self.host_buffer.get())

