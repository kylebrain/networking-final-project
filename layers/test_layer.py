from layers.layer_base import LayerBase, BaseLayerArgs
from queue import Queue

class TestLayerArgs(BaseLayerArgs):
    """
    Holds TestLayer specfic arguments
    """
    def __init__(self):
        """
        If you change the signature of the args __init__ make to reflect when initializing the layers
        """
        self.receive_multiplier = 2
        self.send_decrementer = 1

class TestLayer(LayerBase):
    """
    An example layer to demonstrate the LayerBase
    """
    def __init__(self, layer_id, args):
        """
        A layer __init__ must match the LayerBase signature
        The args parameter type changes for each layer so you can store information about the layer
        """
        super(TestLayer, self).__init__(layer_id, args)
        self.buffer = []

    def process_receive(self, msg):
        """
        Only pushes the messages if there are two in the buffer
        Used the super process_receive to forward to the above receive buffer
        """
        self.buffer.append(self.args.receive_multiplier * msg)
        if len(self.buffer) == 2:
            super(TestLayer, self).process_receive(self.buffer.pop(0))
            super(TestLayer, self).process_receive(self.buffer.pop(0))

    def process_send(self, msg):
        """
        Used the super process_send to forward to below receive buffer
        """
        super(TestLayer, self).process_send(msg - self.args.send_decrementer)