import rot2proG
import serial
import math
import time
import requests
from queue import Queue
from threading import Thread

def _parse_degrees(nmea_data):
    # Parse a NMEA lat/long data pair 'dddmm.mmmm' into a pure degrees value.
    # Where ddd is the degrees, mm.mmmm is the minutes.
    if nmea_data is None or len(nmea_data) < 3:
        return None
    raw = float(nmea_data)
    deg = raw // 100
    minutes = raw % 100
    return deg + minutes/60


def serverThread(threadname, q):

    home_lat = 42.02700680709537
    home_lon = -93.65338786489195
    home_alt = 300
    R = 6372.795477598*1000

    flightID = "0c4dbd3c-6d97-4eb9-afe1-36c069c7b2d5"
    scriptID = "429c4f46-140b-4db4-8cf9-6acc88f5b018"
    postURL = "http://cytracking.com/REST/V1/flight_location"
    postURLRaw = "http://cytracking.com/REST/V1/flight_data_raw"
    latA = home_lat
    lonA = home_lon
    run = True
    lora = serial.Serial(port="COM9", baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=2)
    lora.flushInput()
    lora.flushOutput()
    print("running")
    while run:
        line = ""
        invalid = True
        data = ""
        latB = ''
        lonB = ''
        alt = ''
        rssi = ''
        while invalid:  # Or: while ser.inWaiting():
            if lora.in_waiting:
                print("in waiting: "+str(lora.in_waiting))
                try:
                    line = lora.readline().decode("utf-8")
                    lineToSave = line
                    #print(lineToSave)
                    if("rssi" in lineToSave):
                        rssi = lineToSave.strip("rssi:").strip("\r\n")
                        print(rssi)
                    try:
                        if("rssi" in lineToSave or "GPGGA" in lineToSave):
                            print(lineToSave)
                            params = {'scriptID': scriptID, 'flightID': flightID, 'gps':lineToSave}
                    
                            r = requests.post(url = postURLRaw, data = params, timeout=5)
                            print(r.text)
                    except Exception as e:
                        print(e)
                    line =lineToSave.strip('\n').strip('\r')
                    invalid = False
                except:
                    invalid = True
                    print("bad Unicode")
                    continue
                
                #print(line)
                vals = line.split(',')
            time.sleep(.1)
            #print(line)
            if "GPGGA" not in line:
            
                continue
            try:
                data = [vals[0],_parse_degrees(vals[3]),vals[4],_parse_degrees(vals[5]),vals[6],vals[10]]
            except:
                continue
            if data[2] == "S":
                data[1] = -1* data[1]
            if data[4] == "W":
                data[3] = -1*data[3]
            print(data)

            try:
                latB = float(data[1])#43.02700680709
                lonB = float(data[3])#-94.6533878648
                alt = float(data[5])
                if(latB == 0):
                    invalid = True
                params = {'scriptID': scriptID, 'flightID': flightID, 'time': int(time.time()), 'lat': latB, 'lon': lonB, 'alt':alt, 'rssi': rssi}
                try:
                    r = requests.post(url = postURL, data = params, timeout=5)
                    print(r.text)
                except Exception as e:
                    print(e)
                    print("\n\n\n\n\n NOT SENT \n\n\n\n")
                invalid = False

            except Exception as e:
                print(e)
                print("bad String")

#queue = Queue()
#serverThread = Thread( target=serverThread, args=("Data-Thread", queue) )

#serverThread.start()
#serverThread.join()

serverThread(1,1)