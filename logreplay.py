from cor.api import CORModule, Message


class LogReplay(CORModule):
	def __init__(self, network_adapter=None, *args, **kwargs):
		super().__init__(network_adapter, *args, **kwargs)