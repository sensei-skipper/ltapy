import socket
from . import timestamp as ts

class lta():
	def __init__(self, hostname='localhost', port=8888, reading_directory=None):
		self.hostname = hostname
		self.port = port
		self.s = None
		self.reading_directory = reading_directory
	
	def send_msg(self, msg):
		""" Sends a msg to the LTA board. You should not need to use this method, it is used internally. """
		if self.s is not None:
			raise RuntimeError('Before sending a msg again you have to receive messages from the LTA using the "receive_msg" method!')
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.hostname, self.port))
		self.s.sendall(msg.encode())
		self.s.shutdown(socket.SHUT_WR)
	
	def receive_msg(self, verbose=False):
		""" Receive a msg from the LTA. You should not need to use this method, it is used internally. """
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
		"""
		Send a command to the LTA for execution. 
		msg: str
			The command.
		verbose: bool
			If true then the response from the LTA is printed out in screen.
		Examples:
		lta.do('NROW 10')
		lta.do('read')
		lta.do('exec ccd_erase')
		"""
		self.send_msg(msg)
		data = self.receive_msg(verbose=verbose)
		return data
	
	def erase_and_purge(self):
		self.do('exec ccd_erase')
		self.do('exec ccd_epurge')
	
	def read(self, reading_directory=None, reading_name=None, **current_reading_params):
		"""
		Reads data from the CCD.
		reading_directory: str
			If not provided the default is used.
		reading_name: str
			If not provided a tiemstamp is used.
		**current_reading_params:
			Any param that the LTA accepts. E.g. NCOLS. These params are modified only for the current reading. After reading they are returned to the value they had before calling this function.
		Examples:
		lta.read() # This reads using default configuration and names the file with a timestamp
		lta.read(NROW = 10) # This reads with NROW = 10 and then returns the value of NROW to that prior to the reading.
		lta.read(reading_name='strange_params', NROW=10, NCOL=1000, NSAMP=2)
		lta.read(reading_name='read_using_default_config')
		"""
		if self.reading_directory is None:
			if reading_directory is None:
				raise ValueError('You have to specify a reading directory for saving the files!')
		if len(current_reading_params) != 0:
			current_vals = self.get_params(list(current_reading_params.keys()))
			for key, val in current_reading_params.items():
				self.do(str(key) + ' ' + str(val))
		if reading_name is None:
			reading_name = ts.get_timestamp()
		self.do('name ' + (reading_directory if reading_directory is not None else self.reading_directory) + reading_name + '_')
		self.do('read')
		if len(current_reading_params) != 0:
			idx = 0
			for key, val in current_reading_params.items():
				self.do(str(key) + ' ' + current_vals[idx])
				idx += 1
	
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
				vals[idx] = extra[extra.find(p)+len(p)+3 : extra.find(',', extra.find(p)+len(p)+3)].replace(' ', '')
			elif p in getall:
				vals[idx] = getall[getall.find(p)+len(p)+3 : getall.find('\\', getall.find(p)+len(p)+3)].replace(' ', '')
			else:
				raise ValueError('Cannot find parameter "' + p + '" neither in "lta extra" nor in "lta get all"')
		return vals
