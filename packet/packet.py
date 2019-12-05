
import time

class Packet():
    """
    Includes references to the components of the packets
    Also includes data common to all packets
    """
    def __init__(self):
        self.app = None
        self.transport = None
        self.network = None
        self.link = None
        self.payload = None
        self.type = 0
        self.time_stamp = time.time()

    @classmethod
    def from_copy(cls, other):
        """
        Packet copy constructor
        """
        ret = cls()
        ret.app = other.app
        ret.transport = other.transport
        ret.network = other.network
        ret.link = other.link
        ret.payload = other.payload
        ret.type = other.type
        ret.time_stamp = other.time_stamp
        return ret

    def __str__(self):
        """
        Prints the packet in a readable format including all present packet components
        """
        app_str = ""
        if self.app is not None:
            app_str = str(self.app)
        transport_str = ""
        if self.transport is not None:
            transport_str = str(self.transport)
        network_str = ""
        if self.network is not None:
            network_str = str(self.network)
        link_str = ""
        if self.link is not None:
            link_str = str(self.link)
        return app_str + " & " + transport_str + " & " + network_str + " & " + link_str

class AppPacket():
    def __init__(self, src_id, dest_id, type_id, msg):
        self.type_id = type_id  # 0 for request, 1 for response
        self.msg = msg
        self.src_id = src_id
        self.dest_id = dest_id

    def __str__(self):
        return "App Msg - " + str(self.msg) + ", Type ID - " + str(self.type_id)

class TransportPacket():
    def __init__(self, type_id, tcp_type = 0, seq_num = 0, ack_num = 0):
        self.type_id = type_id  # 0 for TCP, 1 for UDP
        self.tcp_type = tcp_type  # 0 for seq, 1 for ack
        self.seq_num = seq_num
        self.ack_num = ack_num

    def __str__(self):
        ret_str = "Transport "
        if self.type_id == 0:
            ret_str += "TCP "
            if self.tcp_type == 0:
                ret_str += "SEQ %d" % (self.seq_num, )
            else:
                ret_str += "ACK %d" % (self.ack_num, )
        else:
            ret_str += "UDP"
        return ret_str

class LinkPacket():
    def __init__(self, src_id, dest_id):
        self.src_id = src_id
        self.dest_id = dest_id

    def __str__(self):
        return "Link Src - %d, Dest - %d" % (self.src_id, self.dest_id)

class NetworkingPacket():
    def __init__(self, src_id, dest_id):
        self.src_id = src_id
        self.dest_id = dest_id

    def __str__(self):
        return "Network Src - %d, Dest - %d" % (self.src_id, self.dest_id)
