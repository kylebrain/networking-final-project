from load_distributed.layers.layer_base import LayerBase, BaseLayerArgs
import time

class TestTopLayerArgs(BaseLayerArgs):
    pass


class TestTopLayer(LayerBase):
    def __init__(self, simulation_mng, metric_mng, node_data, layer_id, args):
        super().__init__(simulation_mng, metric_mng, node_data, layer_id, args)
        self.host_buffer = []

    def process_receive(self, msg):
        self.host_buffer.append(msg)

    def get_response(self, timeout=None, msg=None):
        """
        Sends a message if specified
        Waits until a response is received and returns the message
        """
        start = time.time()
        if msg is not None:
            self.send_buffer.put(msg)
        while len(self.host_buffer) == 0:
            if timeout is not None and time.time() >= start + timeout:
                return None

        return_msg = self.host_buffer[0]
        self.host_buffer.remove(return_msg)
        return return_msg
