import socket
import datetime
from time import sleep

def get_timestamp():
	"""
	Returns a numeric string with a timestamp. It also halts the execution 
	of the program during 10 micro seconds to ensure that all returned
	timestamps to be different and unique.
	
	Returns
	-------
	str
		String containing the timestamp. Format isYYYYMMDDHHMMSSmmmmmm.
	
	Example
	-------	
	>>> get_timestamp()
	'20181013234913378084'
	>>> [get_timestamp(), get_timestamp()]
	['20181013235501158401', '20181013235501158583']
	"""
	timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
	sleep(10e-6) # This ensures that there will not exist two equal timestamps.
	return timestamp

class lta():
	def __init__(self, hostname='localhost', port=8888):
		self.hostname = hostname
		self.port = port
		self.s = None
		self.reading_directory = None
	
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
			reading_name = get_timestamp()
		self.do('name ' + self.reading_directory + reading_name + '_')
		self.do('read')
