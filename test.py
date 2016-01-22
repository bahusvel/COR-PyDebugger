from cor.api import CORModule, Message
import threading
import time
from logreplay import LogReplay


class Requester(CORModule):

	moduleID = "com.bahus.Requester"

	def sender(self):
		while True:
			time.sleep(1)
			self.messageout(Message("REQUEST", "IS IT OK?"))

	def acknowledge(self, message):
		print(message)

	def __init__(self, network_adapter=None, *args, **kwargs):
		super().__init__(network_adapter, *args, **kwargs)
		self.add_topics({"REQUEST": self.acknowledge})
		self.t = threading.Thread(target=self.sender)
		self.t.start()

with open('data.pickle', 'rb') as f:
	logreplayer = LogReplay(infile=f)
	requester = Requester()
	requester.network_adapter.register_callback("REQUEST", logreplayer)
	logreplayer.network_adapter.register_callback("REQUEST", requester)
	requester.t.join()
