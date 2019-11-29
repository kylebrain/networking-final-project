
class Packet():
    def __init__(self):
				self.app = None
        self.network = None
        self.link = None
        self.payload = None
        self.type = 0
        self.time_stamp = 0

    def __str__(self):
		app_str = ""
		if self,app is not None:
			app_str = str(self.app)
        network_str = ""
        if self.network is not None:
            network_str = str(self.network)
        link_str = ""
        if self.link is not None:
            link_str = str(self.link)
        return app_str + " & " + network_str + " & " + link_str

class AppPacket():
	def __init__(self, type_id, msg):
		self.type_id = type_id
		self.msg = msg

	def get_type(self):
		return self.type_id

	def get_msg(self):
		return self.msg

	def __str__(self):
		return "App Msg - " + self.msg + ", Type ID: " + self.type_id

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
