# ltapy

Use the LTA board from Python, be happy!

## Instalation

For Python 2 run

```
pip install git+https://github.com/sensei-skipper/ltapy.git
```

or for Python 3

```
pip3 install git+https://github.com/sensei-skipper/ltapy.git
```

## Usage

### Before running Python

Before running Python: 

1. Run the *lta daemon* in a terminal. For that purpose you have to run ```./configure.exe``` in the *ltaDaemon* directory, and **do not close this terminal**. Keep it opened.

2. Open a new terminal, go to the directory where you have run the *lta daemon* before and run ```source init_skp_lta_v2.sh```. 

After that you can use *ltapy* in the second terminal (the one in which you run ```source init_skp_lta_v2.sh```). Keep the first terminal with the *lta daemon* opened at all the time.

### Once in Python

You have to run Python in the second terminal of the previous steps in *before running Python*.

1. Import the *ltapy* module:

```Python
import ltapy
```

2. Then create an instance of the ```lta``` class:

```Python
lta = ltapy.lta(reading_directory='/home/me/lta_reads')
```

3. Make readings

```Python
lta.read() # Default file name is a timestamp.
lta.read(NSAMP=247, NCOL=25, NROW=50, reading_name='such_a_measurement', timestamp=True) # This configuration is only used for this reading. After reading, all is brought back to the previous state.
```

4. You can also send any command you like with the ```do``` method:

```Python
lta.do('name /home/me/new_reading_dir')
lta.do('read') # Reading in the old school way
lta.do('NSAMP 100')
```

For more information please see [the source code](https://github.com/SengerM/ltapy/blob/master/ltapy/core.py). 

## Examples

Below there are some examples.

```Python
import ltapy

lta = ltapy.lta(reading_directory='/home/enrico-fermi/dark_matter_definitive_evidence/') # Create an lta instance.
lta.read() # Read using the current LTA configuration. The file name is a timestamp automatically created at the time of calling this function.
lta.read(reading_name='nobel_prize_reading') # The file name contains a timestamp followed by the provided name.
lta.read(reading_name='take_your_timestamp_away', timestamp=False) # The file name has no timestamp
lta.read(timestamp=False) # This will rise an error because we don't know how to name your file...
```

```Python
import ltapy

lta = ltapy.lta(reading_directory='/home/paul-dirac/skipper_ccd_selfies/') # Create an lta instance.
lta.erase_and_purge() # Erase and purge the CCD.
lta.do('NROW 100') # Change the default configuration.
lta.do('NCOL 100') # Change the default configuration.
lta.read(NROW=2100, NCOL=500) # These values of NROW and NCOL are used just for this current reading. After reading they are restored to the value they had before this line.
lta.read() # Read using the default NROW and NCOL values, i.e. this reading will have NROW=100 and NCOL=100
lta.do('read') # Read in the old school fashioned way using the 'do' method.
```

```Python
import ltapy
from time import sleep
import numpy as np

NSAMP = 2**np.arange(10) # Values of NSAMP to sweep.

lta = ltapy.lta(reading_directory='/home/mozzart/what_is_mozzart_doing_here?/')

lta.do('NROW 2000') # Set default NROW.
lta.do('NCOL 500') # Set default NCOL.
lta.read(reading_name='pre_eAp') # Take a reading with current LTA configuration, and store it in "/home/lta-test/Desktop/DarMat/reads/190708/run_c".
lta.erase_and_purge()
lta.read(reading_name='post_eAp') # Another reading.
lta.read(reading_name='post_post_eAp') # Yet another reading.

for nsamp in NSAMP:
	print('Reading with NSAMP ' + str(nsamp))
	lta.read(
		reading_name = 'NSAMP_' + str(NSAMP),
		NSAMP = nsamp, # Change the default NSAMP value, only for this reading. After this it is returned to the previous value.
		NROW = 100 # Change the default NROW value, again only for this reading.
		)
```
