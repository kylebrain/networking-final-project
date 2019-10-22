from layers.layer_base import LayerBase
from queue import Queue

class TestLayer(LayerBase):

    def __init__(self, layer_type, above_layer, layer_id):
        super(TestLayer, self).__init__(layer_type, above_layer, layer_id)
        self.buffer = []

    def process_receive(self, msg):

        self.buffer.append(2 * msg)
        if len(self.buffer) == 2:
            return [self.buffer.pop(0), self.buffer.pop(0)]
        else:
            return []

    def process_send(self, msg):
        return [msg - 1]