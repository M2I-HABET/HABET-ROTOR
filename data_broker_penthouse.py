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

# Create a socket for the server
ip = "192.168.1.31" # this will need to be changed
port_1 = 4444 # The port for it to connect to
port_2 = 6667 # The port for it to open for others to grab data from

test_string = "$Clueboard,42.0267,93.6465,942,30,7465.2,0.67,0.75,0.85".encode('utf-8')


while True:
    

    # we don't use the same name as `syncarr` here (although we could);
    # just to see that `syncarr_tmp` is actually <AutoProxy[syncarr] object>
    # so we also have to expose `__str__` method in order to print its list values!
    syncarr_tmp = manager.syncarr()
    print("syncarr (master):", syncarr, "syncarr_tmp:", syncarr_tmp)
    print("syncarr initial:", syncarr_tmp.__str__())

    # syncarr_tmp.append()

    line = test_string.decode('utf-8')
    vals = line.split(',')
    
    i = 0
    for item in vals :

        syncarr_tmp.append(item)
        print("item: ", item)
        i+= 1
    
    print("number of items set: ", i+1)



    # syncarr_tmp.append(140)
    # syncarr_tmp.append("hello")

    # print("syncarr set:", str(syncarr_tmp))

    # raw_input('Now run b.py and press ENTER')

    # print()
    # print('Changing [0]')
    # syncarr_tmp.__setitem__(0, 250)

    # print('Changing [1]')
    # syncarr_tmp.__setitem__(1, "foo")

    # new_i = raw_input('Enter a new int value for [0]: ')
    # syncarr_tmp.__setitem__(0, int(new_i))

    # raw_input("Press any key (NOT Ctrl-C!) to kill server (but kill client first)".center(50, "-"))


    time.sleep(1)
    test_string = "$Clueboard"
    for i in range(8) :
        test_string += "," + input("input: ")
        if "stop" in test_string :
            break
    if "stop" in test_string :
        break

    print("test_string: ", test_string)
    test_string = test_string.encode('utf-8')
    syncarr_tmp.clear()
    
    
manager.shutdown()








# # Create a socket for the server
# ip = "192.168.1.31" # this will need to be changed
# port_1 = 4444 # The port for it to connect to
# port_2 = 6667 # The port for it to open for others to grab data from

# test_string = "$Clueboard,42.0267,93.6465,942,30,7465.2,0.67,0.75,0.85".encode('utf-8')


# # Begin the data gathering and parsing
# while run:

#     # Buffers for the incoming strings
#     line = ''
#     data = ''
#     latB = ''
#     lonB = ''
#     alt = ''
#     temp = ''
#     pres = ''
#     humi = ''
#     bat = ''
#     rssi = ''

#     # Boolean for if there is an invalid string
#     invalid = True

#     # While the incoming string is invalid
#     while invalid:  # Or: while ser.inWaiting():
#         # If the lora has recieved a message

#         '''
#         if lora.in_waiting:
#             print("in waiting: "+str(lora.in_waiting))
#             try:
#                 # Try to read the line of incoming data
#                 line = lora.readline().decode("utf-8")
#                 lineToSave = line
#                 #print(lineToSave)
#                 if("rssi" in lineToSave):
#                     rssi = lineToSave.strip("rssi:").strip("\r\n")
#                     print(rssi)
#                 # try:
#                 #     if("rssi" in lineToSave or "GPGGA" in lineToSave):
#                 #         print(lineToSave)
#                 #         # params = {'scriptID': scriptID, 'flightID': flightID, 'gps':lineToSave}

#                 #         # We won't need to post anything to the url either
#                 #         # r = requests.post(url = postURLRaw, data = params, timeout=5)
#                 #         print(r.text)
#                 # except Exception as e:
#                 #     print(e)
#                 line =lineToSave.strip('\n').strip('\r')
#                 invalid = False
#             # If reading the line fails then the string is invalid and print an error message to the console
#             except:
#                 invalid = True
#                 print("bad Unicode")
#                 continue
#             '''
            
#             #print(line)

#             # This is the variable that contains all of the incoming strings we want to use
#             # The strings are in the following format: 
#             # $Clueboard,<latitude>,<longitude>,<altitude>,<temperature>,<pressure>,<humidity>,<battery>,<RSSI>
        
#             # Now, all this would need to do is just keep this here and then we can grab the data from this "vals" variable

#         time.sleep(3)

#         # TODO: now to open a socket and place this data here for other things to grab from it





        
# #queue = Queue()
# #serverThread = Thread( target=serverThread, args=("Data-Thread", queue) )

# #serverThread.start()
# #serverThread.join()

# # serverThread(1,1)