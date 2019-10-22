from threading import Thread
from queue import Queue
import abc

class LayerBase():
    def __init__(self, layer_type, above_layer, layer_id):
        self.above_layer = above_layer
        self.layer_id = layer_id

        self.in_buffer = Queue()
        self.out_buffer = Queue()
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
            msg = self.in_buffer.get()
            if self.above_layer is not None:
                msg = self.process_receive(msg)
                print("Layer %d receive: %d" % (self.layer_id, msg))
                self.above_layer.in_buffer.put(msg)
            else:
                # highest layer
                # handle logging
                print(msg)

    def send(self):
        while True:
            msg = self.out_buffer.get()
            if self.below_layer is not None:
                msg = self.process_send(msg)
                print("Layer %d send: %d" % (self.layer_id, msg))
                self.below_layer.out_buffer.put(msg)
            else:
                # lowest layer
                # ultimately transfer to the other physical device
                self.in_buffer.put(msg)

    @abc.abstractmethod
    def process_receive(self, msg):
        pass

    @abc.abstractmethod
    def process_send(self, msg):
        pass