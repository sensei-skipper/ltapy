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

3. Send commands to the *lta board* with the ```do``` attribute:

```Python
lta.do('name /home/me/ccd_reads/')
lta.do('read')
```