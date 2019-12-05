

class MetricManager():
    """
    Includes important metrics about the simulation
    Shared with every layer
    """
    def __init__(self):
        self.total_loss = 0
        self.total_packets = 0
        self.packets_received = 0
        self.delay = []