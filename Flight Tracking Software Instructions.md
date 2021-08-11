# Tracking Software for HABET Flights

Author: Matt Kreul\
Written: 2021-07-05\
Edited: 2021-08-09

These are instructions for running the penthouse computer in order to track a flight for HABET.

## How it works

---

There are two computers being run up at the penthouse.  The first is the main machine (the Windows or Linux computer) and the second is a Raspberry Pi 3 with a LoRa attached to it.  The Raspberry Pi communicates with the LoRa on the payload and receives GPS and atmospheric data.  The Raspberry Pi will then feed that data to the main machine.  On the main machine, a "data broker" will take the information given by the Raspberry Pi and will separate and present them for other scripts to grab onto easily.  

For example, a typical information string of data will come from the payload in the following format:

```
$HAR,<latitude>,<longitude>,<altitude>,<temperature>,<pressure>,<humidity>,<received signal strength indication (rssi)> 
```

with a typical string looking like (sans rssi):

```
$HAR,420266988,-936531391,261586,28.52,43.09,984.9
```

The data broker will then take this information and split it up and save it to a list (array) that other scripts can grab onto easily.  An example of what the parsed data looks like is below:

```
[ $HAR , 420266988 , -936531391 , 261586 , 28.52 , 43.09 , 984.9]
```

(Note that the data are all saved as strings and will need to be parsed into floating point values in order to be any use.  Furthermore, latitude, longitude, and altitude are all saved as integers and will need to be divided by 10000000, 10000000, and 1000 respectively to get the correct value).

Any script that needs this data to run can be created in order to grab the correct information.

## Automatic Tracking of the Payload

---

There are at minimum, four scripts that must be run in order to track a flight.  On the Raspberry Pi, the `lora_server.py`, and on the main machine, `data_broker.py`, `hab_pointer.py`, and `send_data.py`.  If this is a new flight, `get_new_flight.py` must be run as well in order to get a new Flight and Script ID which must be pasted in the proper places in `send_data.py`.  The order that these scripts were listed above is not necessarily the order that they MUST be run so read below for the following instructions.  Unless otherwise specified, all scripts are run on the main machine.

1. If this is a new flight, run `get_new_flight.py` and copy the flight ID and paste it into `send_data.py`.
2. ***Before running any other script*** first run `data_broker.py`.  This starts a server for the Raspberry Pi to connect and send the LoRa data to.
3. Connect to the Raspberry Pi 3 via SSH (use PuTTy on Windows or Remmina on Linux) and run `lora_server.py`.  IP address, username, and password for this device are a need to know basis.  Contact your team lead or project lead for these.
4. Run `hab_pointer.py`.  This enables the rotor to track our payload during the flight.
5. Run `send_data.py`.  This will send the GPS data to the cytrack website for us to track real-time.
6. Run any other scripts that pull data from `data_broker.py`.

To view the flight go to: `cytracking.com/cytrack/<flightID>`

### A Few Notes

After getting `data_broker.py` and `lora_server.py` connected together and running, any script that needs the data from these can be run in any order.  Typically in a flight the priorities are first the data broker and the lora server on the main machine and Raspberry Pi respectively, second is the antenna pointer, and finally is the tracking website.  

## Troubleshooting/Extra Instructions

---

### Manually pointing the Antenna

If you need to manually point the antenna, use `manual_pointing.bat`.  (This simply runs the Python script, `rot2proG.py`.)  

1. Run `manual_pointing.bat`. A command line, `cmd`, window will open.
2. Where it says `COM6:`, (*Note: the com port could change in the future*), type `set`. This will then populate the command line with the parameters to set.
3. Type in your desired `Azimuth`, i.e. bearing, into the command line and press enter.  This number should be in between 0 and 360. North is `0`, East is `90`, South is `180`, and West is `270`.
4. Type in your desired `Elevation`. This number should be between 0 and 180.  Level with the horizon is 0 and completely vertical is 90.

Once these parameters have been set and if there were no errors in input, the rotor will begin to move to the desired position.  If you need to set it again, simply start from number 2 in the above instructions.
