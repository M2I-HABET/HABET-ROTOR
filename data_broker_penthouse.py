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

$Clueboard,<latitude>,<longitude>,<altitude>,<temperature>,<pressure>,<humidity>

'''

logger = multiprocessing.log_to_stderr()
logger.setLevel(logging.INFO)


class MyListManager(multiprocessing.managers.BaseManager):
    pass



def _parse_degrees(nmea_data):
    # Parse a NMEA lat/long data pair 'dddmm.mmmm' into a pure degrees value.
    # Where ddd is the degrees, mm.mmmm is the minutes.
    if nmea_data is None or len(nmea_data) < 3:
        return None
    raw = float(nmea_data)
    deg = raw // 100
    minutes = raw % 100
    return deg + minutes/60

# This holds our data
syncarr = []
def get_arr():
    return syncarr

# print dir([]) # cannot do `exposed = dir([])`!! manually:
MyListManager.register("syncarr", get_arr, exposed=['__getitem__', '__setitem__', '__str__', 'append', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort', 'clear'])

manager = MyListManager(address=('/tmp/mypipe'), authkey=''.encode('utf-8'))
manager.start()


# Start the script
home_lat = 42.02700680709537
home_lon = -93.65338786489195
home_alt = 300
R = 6372.795477598*1000

# dont need the below
# flightID = "0c4dbd3c-6d97-4eb9-afe1-36c069c7b2d5"
# scriptID = "429c4f46-140b-4db4-8cf9-6acc88f5b018"
# postURL = "http://cytracking.com/REST/V1/flight_location"
# postURLRaw = "http://cytracking.com/REST/V1/flight_data_raw"

# these variables are never used
latA = home_lat
lonA = home_lon


run = True

# We will need this for the lora data 
# lora = serial.Serial(port="COM9", baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=2)
# lora.flushInput()
# lora.flushOutput()
# print("running")


ip = "192.168.1.31" # 192.168.1.31 is for testing and 192.168.1.205 is for flight
port = 4440
# print("Do Ctrl+c to exit the program !!")
# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = (ip, port)
s.bind(server_address)
print("bound the server address")
s.listen(5)
conn, addr = s.accept()
print("accepted the connection")

# test_string = "$Clueboard,42.0267,93.6465,942,30,7465.2,0.67,0.75,0.85".encode('utf-8')


while True:
    
    try : 
        data = conn.recv(4096)
        print("\n 1. Server received: ", data.decode('utf-8'), "\n")
        conn.send(data)
        print("\n 2. Server sent : ", data.decode('utf-8'),"\n")
        # we don't use the same name as `syncarr` here (although we could);
        # just to see that `syncarr_tmp` is actually <AutoProxy[syncarr] object>
        # so we also have to expose `__str__` method in order to print its list values!
        syncarr_tmp = manager.syncarr()
        print("syncarr (master):", syncarr, "syncarr_tmp:", syncarr_tmp)
        print("syncarr initial:", syncarr_tmp.__str__())

        line = data.decode('utf-8')
        vals = line.split(',')
        
        i = 0
        # Append the new items in vals
        for item in vals :
            syncarr_tmp.append(item)
            print("item: ", item)
            i+= 1
        
        print("number of items set: ", i+1)
        print(syncarr_tmp)


        time.sleep(1)

        # test_string = "$Clueboard"
        # for i in range(8) :
        #     test_string += "," + input("input: ")
        #     if "stop" in test_string : #TODO: remember to remove this for the flight
        #         break
        # if "stop" in test_string :
        #     break

        # print("test_string: ", test_string)
        # test_string = test_string.encode('utf-8')
        syncarr_tmp.clear()
    except Exception as e :
        print(e)

    
    
manager.shutdown()








