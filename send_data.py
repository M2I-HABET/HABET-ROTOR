import rot2proG
import serial
import math
import time
import requests
from queue import Queue
from threading import Thread
import multiprocessing
import multiprocessing.managers
import logging
logger = multiprocessing.log_to_stderr()
logger.setLevel(logging.INFO)



def _parse_degrees(nmea_data):
    # Parse a NMEA lat/long data pair 'dddmm.mmmm' into a pure degrees value.
    # Where ddd is the degrees, mm.mmmm is the minutes.
    if nmea_data is None or len(nmea_data) < 3:
        return None
    raw = float(nmea_data)
    deg = raw // 100
    minutes = raw % 100
    return deg + minutes/60

class MyListManager(multiprocessing.managers.BaseManager):
    pass

MyListManager.register("syncarr")

def main():
    # Start Script
    print("Started Send Data script (sending data from the penthouse to the tracking website)")

    # Constants
    # home_lat = 42.02700680709537
    # home_lon = -93.65338786489195
    # home_alt = 350
    # R = 6372.795477598*1000
    flightID = "4a2c6d0e-47bc-4c29-a029-0ece360d2b5e" # You will want to change this every flight
    scriptID = "b80b32af-3025-4b1c-b9f1-a15909c63958"
    postURL = "http://cytracking.com/REST/V1/flight_location"
    postURLRaw = "http://cytracking.com/REST/V1/flight_data_raw"

    # manager = MyListManager(address=('/tmp/mypipe'), authkey=''.encode('utf-8')) #for UNIX
    manager = MyListManager(address=('192.168.1.205', 8080), authkey=''.encode('utf-8'))
    manager.connect()
    syncarr = manager.syncarr()

    # print ("arr = %s" % (dir(syncarr)))

    # note here we need not bother with __str__ 
    # syncarr can be printed as a list without a problem:
    print ("List at start:", syncarr)

    print("Running")
    while True:
        arr_data = []
        invalid = True
        data = ""
        latB = ''
        lonB = ''
        alt = ''
        rssi = ''
        while invalid:
            
            try:
                # set data to syncarr since it is easier to work with when you set a variable to it
                arr_data = syncarr
                # change the given format to the intended data
                latB = float(arr_data[1])/10000000
                lonB = float(arr_data[2])/10000000
                alt = float(arr_data[3])/1000
                print("lat: ", latB)
                print("lon: ", lonB)
                print("alt: ", alt)
                try :
                    print("Raw Data: ", arr_data)
                    params = {'scriptID': scriptID, 'flightID': flightID, 'gps':arr_data}
                    r = requests.post(url=postURLRaw, data=params, timeout=5)

                except Exception as e:
                    print(e)
                    print("\n\n\n\n\n postURLRaw NOT SENT \n\n\n\n")
                try:
                    latB = float(arr_data[1])/10000000
                    lonB = float(arr_data[2])/10000000
                    alt = float(arr_data[3])/1000
                    if(latB == 0):
                        invalid = True
                    params = {'scriptID': scriptID, 'flightID': flightID, 'time': int(time.time()), 'lat': latB, 'lon': lonB, 'alt':alt, 'rssi': "none"}
                    try:
                        r = requests.post(url = postURL, data = params, timeout=5)
                        print(r.text)
                    except Exception as e:
                        print(e)
                        print("\n\n\n\n\n postURL NOT SENT \n\n\n\n")
                    invalid = False

                except Exception as e:
                    print(e)
                    print("bad String")

                
                invalid = False
            except:
                print("syncarr may not be set, or no new data")
                continue
            finally :
                time.sleep(1)
            

            

if __name__ == '__main__':
    main()

