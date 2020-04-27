from threading import Thread
from queue import Queue
import abc

class BaseLayerArgs():
    """
    Inherented by layer args
    """
    pass

class LayerBase():
    """
    Interface for each layer
    Processes each packet the layer sends and receives
    See test_layer.py for an example on how to create a layer
    """
    def __init__(self, simulation_mng, metric_mng, node_data, layer_id, args):
        """
        Spawns the threads to retreive and process message from the send and receive buffers
        Arguments
            simulation_mng - used to stop the simulation when a node goes offline
            metric_mng - used to keep track of loss and delay
            note_data - initialized node data including ID and battery life
            layer_id - unique id of the layer
            args - specialized arguments defined by each argument
        """
        self.layer_id = layer_id

        self.receive_buffer = Queue()
        self.send_buffer = Queue()
        self.above_layer = None
        self.below_layer = None

        # Type is BaseLayerArgs
        self.args = args

        self.node_data = node_data
        self.simulation_mng = simulation_mng
        self.metric_mng = metric_mng

        receive_thread = Thread(target=self.receive)
        receive_thread.daemon = True
        send_thread = Thread(target=self.send)
        send_thread.daemon = True

        receive_thread.start()
        send_thread.start()

    def receive(self):
        """
        When a packet is found in the receive buffer, the layer processes it
        """
        while True:
            msg = self.receive_buffer.get()
            #print("Layer %d (id=%d) receive: %s" % (self.layer_id, self.node_data.id, msg))
            self.process_receive(msg)

    def send(self):
        """
        When a packet is found in the sent buffer, the layer processes it
        """
        while True:
            msg = self.send_buffer.get()
            #print("Layer %d (id=%d) send: %s" % (self.layer_id, self.node_data.id, msg))
            self.process_send(msg)

    @abc.abstractmethod
    def process_receive(self, msg):
        """
        Processes msg which was retreived from the receive buffer
        """
        if self.above_layer is not None:
            self.above_layer.receive_buffer.put(msg)
        else:
            raise ValueError("Default process_receive called with no above layer")

    @abc.abstractmethod
    def process_send(self, msg):
        """
        Processes msg which was retreived from the send buffer
        """
        if self.below_layer is not None:
            self.below_layer.send_buffer.put(msg)
        else:
            raise ValueError("Default process_send called with no below layer")
