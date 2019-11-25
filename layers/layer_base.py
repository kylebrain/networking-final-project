from threading import Thread
from queue import Queue
import abc

class LayerBase():
    def __init__(self, layer_type, above_layer, layer_id):
        self.above_layer = above_layer
        self.layer_id = layer_id

        self.receive_buffer = Queue()
        self.send_buffer = Queue()
        self.below_layer = None

        # TODO: have the factory set the below layer
        if self.layer_id > 0:
            self.below_layer = layer_type(layer_type, self, layer_id - 1)

        receive_thread = Thread(target=self.receive)
        receive_thread.daemon = True
        send_thread = Thread(target=self.send)
        send_thread.daemon = True

        receive_thread.start()
        send_thread.start()

    def receive(self):
        while True:
            if self.above_layer is not None:
                msg = self.receive_buffer.get()
                above_msgs = self.process_receive(msg)

                for above_msg in above_msgs:
                    print("Layer %d receive: %d" % (self.layer_id, above_msg))
                    self.above_layer.receive_buffer.put(above_msg)

    def send(self):
        while True:
            msg = self.send_buffer.get()
            if self.below_layer is not None:
                below_msgs = self.process_send(msg)

                for below_msg in below_msgs:
                    print("Layer %d send: %d" % (self.layer_id, below_msg))
                    self.below_layer.send_buffer.put(below_msg)
            else:
                # lowest layer
                # ultimately transfer to the other physical device
                self.receive_buffer.put(msg)

    @abc.abstractmethod
    def process_receive(self, msg):
        pass

    @abc.abstractmethod
    def process_send(self, msg):
        pass