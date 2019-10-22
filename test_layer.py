from layer_base import LayerBase

class TestLayer(LayerBase):
    def process_receive(self, msg):
        return 2 * msg

    def process_send(self, msg):
        return msg - 1