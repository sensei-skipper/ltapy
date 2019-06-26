# ltapy
Python wrapper to use with the LTA board

## Instalation

Make sure you have ```pip``` installed. Then run:

```
pip install git+https://github.com/SengerM/ltapy
```

## Usage

### Before running Python

Before running Python: run the *lta daemon* in a terminal. Then initialize the lta. Once the lta is responding, then we can go to Python.

### In Python

1. Import the *ltapy* module:

```Python
import ltapy
```

2. Then create an instance of the ```lta``` class:

```Python
lta = ltapy.lta()
```

3. Send commands to the *lta board* with the ```do``` method:

```Python
lta.do('name /home/me/ccd_reads/')
lta.do('read')
```

There are methods that do common stuff automatically. For example

```Python
lta.erase_and_purge()
```

or

```Python
lta.read()
```

For usage see [the source code](https://github.com/SengerM/ltapy/blob/master/ltapy/core.py). A complete usage example:

```Python
import ltapy

lta = ltapy.lta() # Create an lta instance.
lta.read(reading_directory='/home/lta-test/Desktop/DarMat/reads/') # Launch a reading and specify the reading directory, where the files will be stored.
lta.erase_and_purge() # Erase and purge the CCD.
lta.read() # The reading directory is the same as before.
```
