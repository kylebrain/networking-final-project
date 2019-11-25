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
    def __init__(self, layer_id, args):
        """
        Arguments
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

        receive_thread = Thread(target=self.receive)
        receive_thread.daemon = True
        send_thread = Thread(target=self.send)
        send_thread.daemon = True

        receive_thread.start()
        send_thread.start()

    def receive(self):
        """
        When a packet is found in the receive buffer, the layer processes and pushes it to the above layer
        If there is no above_layer, packets will just sit in the receive buffer
        """
        while True:
            if self.above_layer is not None:
                msg = self.receive_buffer.get()
                above_msgs = self.process_receive(msg)

                for above_msg in above_msgs:
                    print("Layer %d receive: %d" % (self.layer_id, above_msg))
                    self.above_layer.receive_buffer.put(above_msg)

    def send(self):
        """
        When a packet is found in the sent buffer, the layer processes and pushes it to the below layer
        If there is below_layer, packets are transmitted according the the transmit function
        """
        while True:
            msg = self.send_buffer.get()
            if self.below_layer is not None:
                below_msgs = self.process_send(msg)

                for below_msg in below_msgs:
                    print("Layer %d send: %d" % (self.layer_id, below_msg))
                    self.below_layer.send_buffer.put(below_msg)
            else:
                print("Layer %d transmit: %d" % (self.layer_id, msg))
                self.transmit(msg)

    @abc.abstractmethod
    def process_receive(self, msg):
        """
        Processes msg which was retreived from the receive buffer
        Returns a list of packets to send to the above layer
        """
        return [msg, ]

    @abc.abstractmethod
    def process_send(self, msg):
        """
        Processes msg which was retreived from the send buffer
        Returns a list of packets to send to the below layer
        """
        return [msg, ]

    @abc.abstractmethod
    def transmit(self, msg):
        """
        Used by a tranmitting layer
        Allowed to transfer a message from the send buffer to another node's receive buffer
        """
        pass