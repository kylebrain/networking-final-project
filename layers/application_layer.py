from layers.layer_base import LayerBase, BaseLayerArgs
from queue import Queue

class ApplicationLayerArgs(BaseLayerArgs):
    pass

class ApplicationLayer(LayerBase):
    def __init__(self, node_data, layer_id, args):
        super(ApplicationLayer, self).__init__(node_data, layer_id, args)
        self.host_buffer = Queue()


    def process_receive(self, msg):
        self.host_buffer.put(msg)