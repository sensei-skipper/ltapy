# ltapy

Command the LTA board from Python, be happy!

## Instalation

Make sure you have ```pip``` installed. Then run:

```
pip install git+https://github.com/SengerM/ltapy
```

## Usage

### Before running Python

Before running Python: run the *lta daemon* in a terminal. Then initialize the lta. Once the lta is responding, then we can go to Python. I.e. you first have to run ```./configure.exe``` in the *ltaDaemon* directory and ```source init_skp_lta_v2.sh```. After that you can use *ltapy*.

### Once in Python

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

lta = ltapy.lta(reading_directory='/home/me/dark_matter_measurements/') # Create an lta instance.
lta.erase_and_purge() # Erase and purge the CCD.
lta.read(NROW=2100, NCOL=500) # Read with NROW=2100 and NCOL=500 to make sure the whole active area is cleaned.
lta.read() # Read using the default NROW and NCOL values.
lta.do('NROW 10') # Change the value of NROW.
lta.do('read') # Read using the 'do' method.
```
