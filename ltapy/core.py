import socket

class lta():
	def __init__(self, hostname='localhost', port=8888):
		self.hostname = hostname
		self.port = port
		self.s = None
	
	def write(self, msg):
		if self.s is not None:
			raise RuntimeError('Before writing again you have to read!')
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.hostname, self.port))
		self.s.sendall(msg.encode())
		self.s.shutdown(socket.SHUT_WR)
	
	def read(self, verbose=False):
		if self.s is None:
			raise RuntimeError('Before reading an answer you have to write a command!')
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
		self.write(msg)
		data = self.read(verbose=verbose)
		return data
