
class Packet():
    def __init__(self):
        self.network = None
        self.link = None
        self.payload = None
        self.type = 0
        self.time_stamp = 0

    def __str__(self):
        network_str = ""
        if self.network is not None:
            network_str = str(self.network)
        link_str = ""
        if self.link is not None:
            link_str = str(self.link)
        return network_str + " & " + link_str

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
