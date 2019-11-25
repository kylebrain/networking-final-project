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
        Return a list of msgs, can return a list so a layer can wait to push multiple packets at a time
        """
        self.buffer.append(args.receive_multiplier * msg)
        if len(self.buffer) == 2:
            return [self.buffer.pop(0), self.buffer.pop(0)]
        else:
            return []

    def process_send(self, msg):
        """
        Return a list of msgs, can return a list so a layer can wait to send multiple packets at a time
        """
        return [args.send_decrementer - 1]

    def transmit(self, msg):
        """
        Only needs to be defined for the lowest layer (below_layer is None)
        Used to transfer data from a node's send_buffer to another node's receive_buffer
        """
        self.receive_buffer.put(msg)