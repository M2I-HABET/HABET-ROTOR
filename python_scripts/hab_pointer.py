# Author: Matt Plewa (Modified by Matt Kreul)
from os import system
import rot2proG
import serial
import math
import time
import requests
import json
import multiprocessing
import multiprocessing.managers
import logging


'''
This is a script to point the HABET antenna to the payload during flights.  This grabs data that was parsed by 
"data_broker_penthouse.py".  From this, it will automatically turn the rotor to the direction of the payload.  

For this to work, the data broker (data_broker_penthouse.py) needs to be running first. Otherwise, the script 
will attempt to grab data from an object that does not exist.
'''
logger = multiprocessing.log_to_stderr()
logger.setLevel(logging.DEBUG)


class MyListManager(multiprocessing.managers.BaseManager):
    pass

MyListManager.register("syncarr")

def main(): 

    # Start Script
    print("HAB Pointer started")

    # Constants
    home_lat = 42.02700680709537
    home_lon = -93.65338786489195
    home_alt = 350
    R = 6372.795477598*1000
    latA = home_lat
    lonA = home_lon

    # Start the rotor
    rot = rot2proG.Rot2proG("/dev/ttyUSB0")

    
    manager = MyListManager(address=('/tmp/mypipe'), authkey=''.encode('utf-8')) #for UNIX
    # manager = MyListManager(address=('192.168.1.205', 8080), authkey=''.encode('utf-8'))
    manager.connect()
    syncarr = manager.syncarr()

    # note here we need not bother with __str__ 
    # syncarr can be printed as a list without a problem:
    print ("List at start:", syncarr)
    # syncarr.append(30)
    # print ("List now:", syncarr)

    while True:
        print("===HAB POINTER===")
        line = ""
        invalid = True
        
        data = ""
        latB = ''
        lonB = ''
        alt = ''
        
        # While there is no new valid data given
        while invalid:  # Or: while ser.inWaiting():
            print("Attempting to get data for rotor")
            try:
                # set data to syncarr since it is easier to work with when you set a variable to it
                data = syncarr
                # change the given format to the intended 
                latB = float(data[1])/10000000
                lonB = float(data[2])/10000000
                alt = float(data[3])/1000
                print("lat: ", latB)
                print("lon: ", lonB)
                print("alt: ", alt)

                invalid = False
            except:
                print("syncarr may not be set, or no new data")
                continue
            finally :
                time.sleep(1)
            
            
                    
        try:
            
            # Do all the math
            # DO NOT CHANGE THIS UNLESS YOU KNOW WHAT YOU'RE DOING
            phi1 = latA*math.pi/180
            phi2 = latB*math.pi/180
            dphi = (latB-latA)*math.pi/180
            dlamb = (lonB-lonA)*math.pi/180
            
            a = math.sin(dphi/2)*math.sin(dphi/2)+math.cos(phi1)*math.cos(phi2)*math.sin(dlamb/2)*math.sin(dlamb/2)
            
            c = 2*math.atan(math.sqrt(a)/math.sqrt(1-a))
            distance = R*c

            x = math.cos(latB*math.pi/180)*math.sin(math.pi/180*(lonA-lonB))
            y = math.cos(latA*math.pi/180)*math.sin(math.pi/180*latB)-math.sin(math.pi/180*latA)*math.cos(math.pi/180*latB)*math.cos(math.pi/180*(lonA-lonB))
        
            az =  -180/math.pi*math.atan(x/y)
            dla = latB-latA
            dlo = lonB-lonA
            az = abs(az)%90
            #print(az)
            #print("az"+str(az))
            #print(dla)
            #print(dlo)
            if(dla<0 and dlo>0):
                az = 180-az
            if(dla<0 and dlo<0 and az<270):
                az = 180+az
            if(dla>0 and dlo<0 and (az<180 or az>270)):
                az = 360-az
            if(dla>0 and dlo>0 and (az<90 or az>180)):
                az = az
                
                
            el = 180/math.pi*math.atan(int(alt-home_alt)/distance)
            
            # Print the elevation, azimuth (angle the rotor is at), and distance from the antenna to the payloaad
            print("Elevation: "+ str(el))
            print("Azimuth: " + str(az))
            print("Distance: "+ str(distance))
            if(el<0):
                el = 0
            
            time.sleep(2)
            rot.set(az,el)
        except:
            e = system.exc_info()[0]
            print(e)

if __name__ == '__main__':
    main()
        