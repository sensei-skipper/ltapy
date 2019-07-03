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
		String containing the timestamp. Format is yyMMDDHHMMSS.
	
	Example
	-------	
	>>> get_timestamp()
	'190703131952'
	>>> [get_timestamp(), get_timestamp()]
	['190703132007', '190703132008']

	"""
	timestamp = datetime.datetime.now().strftime('%y%m%d%H%M%S')
	sleep(1) # This ensures that there will not exist two equal timestamps.
	return timestamp
