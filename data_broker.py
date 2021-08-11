import rot2proG
import serial
import math
import time
import requests
import socket
from queue import Queue
from threading import Thread
import multiprocessing
import multiprocessing.managers
import logging

'''
This is a script designed to parse and hold data tracking data for other programs to grab from.

It will grab data from the GPS's lora, from the RPi, and from the satellite tracker.

$HAR,<latitude>,<longitude>,<altitude>,<temperature>,<pressure>,<humidity>,<rssi (not implemented)>

Most of this code was borrowed followed from this StackOverflow answer:
    https://stackoverflow.com/questions/1829116/how-to-share-variables-across-scripts-in-python

'''

logger = multiprocessing.log_to_stderr()
logger.setLevel(logging.DEBUG)


class MyListManager(multiprocessing.managers.BaseManager):
    pass


# This holds our data
# TODO: consider changing this to a dict with the keys being the names of the data
syncarr = []
def get_arr():
    return syncarr

# We need a main for Windows machines to operate properly.  Unix does not need this but it's better to keep it the same across
# all systems
def main() :
    # Start Script
    print("Data Broker started")
    # Constants
    ip = "192.168.1.205" # 192.168.1.31 is for testing and 192.168.1.205 is for flight
    port_parse = 8080 # port for scripts to attach to
    port_lora = 4440 # port for getting data from the lora
    # home_lat = 42.02700680709537
    # home_lon = -93.65338786489195
    # home_alt = 300
    # R = 6372.795477598*1000

    # Syncarr
    print("Create synarr in register")
    MyListManager.register("syncarr", get_arr, exposed=['__getitem__', '__setitem__', '__str__', 'append', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort', 'clear'])
    print("Syncarr created!")
    # manager = MyListManager(address=('/tmp/mypipe'), authkey=''.encode('utf-8')) # for Unix
    manager = MyListManager(address=(ip, port_parse), authkey=''.encode('utf-8'))
    print("Server address for scripts to attach to: ", ip, ":", port_parse)
    manager.start()

    # LoRa Server Start
    # Create a UDP socket for the lora data
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the port
    server_address = (ip, port_lora)
    s.bind(server_address)
    print("Bound the LoRa server address")
    s.listen(5)
    conn, addr = s.accept()
    print("Accepted the LoRa connection (RPi connected to machine)")

    print("Start While")
    while True:
        print("===DATA BROKER===")
        try : 
            # Saving syncarr as another variable makes it a little easier to work with
            syncarr_tmp = manager.syncarr()
            # print("syncarr (master):", syncarr, "syncarr_tmp:", syncarr_tmp)
            # print("syncarr initial:", syncarr_tmp.__str__())

            # Attempt to get new data from the RPi LoRa Server
            data = conn.recv(4096)
            print("\n 1. Server received: ", data.decode('utf-8'), "\n")
            conn.send(data)
            print("\n 2. Server sent : ", data.decode('utf-8'),"\n")

            # If there is new data, then we can clear the current syncarr
            syncarr_tmp.clear()

            # Get the data and "tokenize" it
            line = data.decode('utf-8')
            vals = line.split(',')
            
            # i is to check to see how many items the LoRa has sent 
            i = 0
            # Append the new items in vals to syncarr and print the values
            for item in vals :
                syncarr_tmp.append(item)
                print("item: ", item) 
                i+= 1
            
            print("number of items set: ", i+1)

            # Print what syncarr was set to
            print(syncarr_tmp)

            # After setting syncarr, clear it so we can append it easier 
            # We will leave it set for a second so other scripts can grab the most recent data
            # TODO: change this to setting the variable indices
            # TODO: change so that it will only clear syncarr when there is new data to set
            
            # Only grab new data every 1 second or so 
            time.sleep(1)
            # syncarr_tmp.clear()
        except Exception as e :
            print(e)

        
        
    manager.shutdown()

if __name__ == '__main__':
    main()







