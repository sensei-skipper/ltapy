import socket
import os

class lta():
    def __init__(self, hostname='localhost', port=8888, reading_directory=None):
        self.hostname = hostname
        self.port = port
        self.reading_directory = reading_directoray

        self.img_sequencer = 'sequencer_C.xml'
        self.clean_sequencer = 'sequencer_clear_C.xml'

    
    def sendMsg(self, msg, verbose=False):
        """ Sends a msg to the LTA board. You should not need to use this method, it is used internally. """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.hostname, self.port))
        sock.sendall(msg.encode())
        sock.shutdown(socket.SHUT_WR)

        data = []
        while 1:
            data = data + [sock.recv(2048)]
            if verbose:
                print(str(data[-1]))
            if not data[-1]:
                break
        
        sock.close()
        return data
   

    def do(self, msg, verbose=False):
        """
        Send a command to the LTA for execution. 
        msg: str
                The command.
        verbose: bool
                If true then the response from the LTA is printed out in screen.
        """
        data = self.sendMsg(msg, verbose=verbose)
        return data
   

    def NCOL(self, ncol, verbose=False):
        """ Set the number of columns """
        msg = "NCOL {0}".format(ncol)
        data = self.sendMsg(msg, verbose=verbose)
        return data


    def NROW(self, nrow, verbose=False):
        """ Set the number of rows """
        msg = "NROW {0}".format(nrow)
        data = self.sendMsg(msg, verbose=verbose)
        return data


    def set(self, var, val, verbose=False):
        """ Set a variables to some value in the lta """
        msg = "set {0} {1}".format(var, val)
        data = self.sendMsg(msg, verbose=verbose)
        return data


    def seq(self, sequencer, verobse=False):
        """ Load a sequencer to the LTA """
        msg = "seq {0}".format(sequencer)
        data = self.sendMsg(msg, verbose=verbose)
        return data


    def name(self, NAME, verobse=False):
        msg = "name {0}".format(NAME)
        data = self.sendMsg(msg, verbose=verbose)
        return data


    def erase_and_purge(self):
        """ Erease and Purge the CCD pixles """
        self.sendMsg('exec ccd_erase')
        self.sendMsg('exec ccd_epurge')


    def read(self):
        """ Reads data from the CCD """
        self.sendMsg('read')


    def runseq(self):
        """ Runs the sequencer without taking data """
        # If you run a sequencer ment to take data, You will run tinto problems
        # Be carefull which sequencer you use with thin
        self.sendMsg('runseq')


    def get_params(self, params):
        """
        Return the values of the parameters in the list <params>.
        Example:
        lta.get_params(['NCOLS', 'NROWS'])
        """
        extra = str(self.sendMsg('extra'))
        getall = str(self.sendMsg('get all'))
        vals = [None]*len(params)
        for idx,p in enumerate(params):
            if p in extra:
                vals[idx] = extra[extra.find(p)+len(p)+3 : extra.find(',', extra.find(p)+len(p)+3)].replace(' ', '')
            elif p in getall:
                vals[idx] = getall[getall.find(p)+len(p)+3 : getall.find('\\', getall.find(p)+len(p)+3)].replace(' ', '')
            else:
                raise ValueError('Cannot find parameter "' + p + '" neither in "lta extra" nor in "lta get all"')
        return vals

