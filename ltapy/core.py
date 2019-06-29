import socket
from . import timestamp as ts

class lta():
	def __init__(self, hostname='localhost', port=8888, reading_directory=None):
		self.hostname = hostname
		self.port = port
		self.s = None
		self.reading_directory = reading_directory
	
	def send_msg(self, msg):
		if self.s is not None:
			raise RuntimeError('Before sending a msg again you have to receive messages from the LTA using the "receive_msg" method!')
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.hostname, self.port))
		self.s.sendall(msg.encode())
		self.s.shutdown(socket.SHUT_WR)
	
	def receive_msg(self, verbose=False):
		if self.s is None:
			raise RuntimeError('Before receiving a msg you have to send a msg using the "send_msg" method!')
		data = []
		while 1:
			data = data + [self.s.recv(2048)]
			if verbose:
				print(str(data[-1]))
			if not data[-1]:
				break
		self.s.close()
		self.s = None
		return data
	
	def do(self, msg, verbose=False):
		self.send_msg(msg)
		data = self.receive_msg(verbose=verbose)
		return data
	
	def erase_and_purge(self):
		self.do('exec ccd_erase')
		self.do('exec ccd_epurge')
	
	def read(self, reading_directory=None, reading_name=None):
		if self.reading_directory is None:
			if reading_directory is None:
				raise ValueError('You have to specify a reading directory for saving the files!')
			self.reading_directory = reading_directory
		if reading_name is None:
			reading_name = ts.get_timestamp()
		self.do('name ' + self.reading_directory + reading_name + '_')
		self.do('read')
	
	def get_params(self, params):
		"""
		Return the values of the parameters in the list <params>.
		Example:
		lta.get_params(['NCOLS', 'NROWS'])
		"""
		extra = str(self.do('extra'))
		getall = str(self.do('get all'))
		vals = [None]*len(params)
		for idx,p in enumerate(params):
			if p in extra:
				vals[idx] = extra[extra.find(p)+len(p)+3 : extra.find(',', extra.find(p)+len(p)+3)]
			elif p in getall:
				vals[idx] = getall[getall.find(p)+len(p)+3 : getall.find('\\', getall.find(p)+len(p)+3)]
			else:
				raise ValueError('Cannot find parameter "' + p + '" neither in "lta extra" nor in "lta get all"')
		return vals
