import socket
from . import timestamp as ts
import os

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
        
        def NCOL(self, ncol):
            """ Set the number of columns """
            msg = "NCOL {0}".format(ncol)
            self.send_msg(msg)
            data = self.receive_msg(verbose=verbose)
            return data

        def NROW(self, nrow):
            """ Set the number of rows """
            msg = "NROW {0}".format(nrow)
            self.send_msg(msg)
            data = self.receive_msg(verbose=verbose)
            return data
        
        def set(self, var, val, verbose=False):
            """ Set a variables to some value in the lta """
            msg = "set {0} {1}".format(var, val)
            self.send_msg(msg)
            data = self.receive_msg(verbose=verbose)
            return data

        def seq(self, sequencer):
            """ Load a sequencer to the LTA """
            msg = "seq {0}".format(sequencer)
            self.send_msg(msg)
            data = self.receive_msg(verbose=verbose)
            return data

        def name(self, NAME):
            msg = "name {0}".format(NAME)
            self.send_msg(msg)
            data = self.receive_msg(verbose=verbose)
            return data

	def erase_and_purge(self):
		self.do('exec ccd_erase')
		self.do('exec ccd_epurge')
	
        def read(self):
		""" Reads data from the CCD """
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
				vals[idx] = extra[extra.find(p)+len(p)+3 : extra.find(',', extra.find(p)+len(p)+3)].replace(' ', '')
			elif p in getall:
				vals[idx] = getall[getall.find(p)+len(p)+3 : getall.find('\\', getall.find(p)+len(p)+3)].replace(' ', '')
			else:
				raise ValueError('Cannot find parameter "' + p + '" neither in "lta extra" nor in "lta get all"')
		return vals
