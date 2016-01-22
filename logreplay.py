from cor.api import CORModule
import pickle
import time
import threading


class MessageRepr:
	def __init__(self, timewait, message):
		super().__init__()
		self.timewait = timewait
		self.message = message


class LogReplay(CORModule):

	moduleID = "com.bahus.LogReplay"

	def log(self, message):
		ctime = time.time()
		mrepr = MessageRepr(ctime - self.otime, message)
		self.otime = ctime
		self.pickler.dump(mrepr)
		self.outfile.flush()
		print("Pickled " + str(message))

	def unpickle_iter(self):
		try:
			while True:
				yield self.unpickler.load()
		except EOFError:
			raise StopIteration

	def play(self):
		for mrepr in self.unpickle_iter():
			time.sleep(mrepr.timewait)
			self.messageout(mrepr.message)
		print("Finished replay")

	def __init__(self, outfile=None, infile=None, network_adapter=None, *args, **kwargs):
		super().__init__(network_adapter, *args, **kwargs)
		if infile is None and outfile is None:
			raise Exception("No file was specified, cannot playback or record")
		if infile is not None:
			print("Going to do playback")
			self.unpickler = pickle.Unpickler(infile)
			self.it = threading.Thread(target=self.play)
			self.it.start()
		if outfile is not None:
			print("Going to record")
			self.add_topics({"ANY": self.log})
			self.pickler = pickle.Pickler(outfile)
			self.otime = time.time()
			self.outfile = outfile
