# Tracking Software for HABET Flights
Author: Matt Kreul\
Written: 2021-07-05\
Edited: 2021-08-04

These are instructions for running the penthouse computer in order to track a flight for HABET. 

## How it works
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
(Note that the data are all saved as strings and will need to be parsed into floating point values in order to be any use.  Furthermore, latitude, longitude, and altitude are all saved aas integers and will need to be divided by 10000000, 10000000, and 1000 respectively to get the correct value).

Any script that needs this data to run can be created in order to grab the correct information.

## Instructions 

There are at minimum, four scripts that must be run in order to track the flight.  On the Raspberry Pi, the `lora_server.py`, and on the main machine, `data_broker.py`, `hab_pointer.py`, and `send_data.py`.  If this is a new flight, `get_new_flight.py` must be run as well in order to get a new Flight and Script ID which must be pasted in the proper places in `send_data.py`.  The order that these scripts were listed above is not necessarily the order that they MUST be run so read below for the following instructions.  Unless otherwise specified, all scripts are run on the main machine.

1. If this is a new flight, run `get_new_flight.py` and copy the flight ID and paste it into `send_data.py`.
2. *Before running any other script* first run the `data_broker.py`.  This starts a server for the Raspberry Pi to connect to and send the LoRa data to.
3. Connect to the Raspberry Pi 3 via SSH (use PuTTy on Windows or Remmina on Linux) and run `lora_server.py`.  IP address, username, and password for this device are a need to know basis.  Contact your team lead or project lead for these. 
4. Run `hab_pointer.py`.  This enables the rotor to track our payload during the flight.
5. Run `send_data.py`.  This will send the GPS data to the cytrack website for us to track real-time.

To view the flight go to: `cytracking.com/cytrack/<flightID>`