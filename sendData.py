import rot2proG
import serial
import math
import time
import requests

home_lat = 42.02700680709537
home_lon = -93.65338786489195
home_alt = 300
R = 6372.795477598*1000

flightID = "58579ff6-c2ec-4650-a930-65f335929b35"
scriptID = "429c4f46-140b-4db4-8cf9-6acc88f5b018"
postURL = "http://127.0.0.1:8000/REST/V1/flight_location"
latA = home_lat
lonA = home_lon
run = True
vCom = serial.Serial(port="COM11", baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=2)
vCom.flushInput()
while run:
    line = ""
    invalid = True
    print("start while")
    data = ""
    latB = ''
    lonB = ''
    alt = ''
    while invalid:  # Or: while ser.inWaiting():
        if vCom.in_waiting:
            line = vCom.readline()
        time.sleep(.1)
        try:
            if "NONE" in line.decode("utf-8"):
                print("NONE")
            elif line != "":
                print(line)
                
                data = line.decode("utf-8").strip("\n").split(",")[0:7]
                print(data)
                latB = float(data[1])#43.02700680709
                lonB = float(data[3])#-94.6533878648
                alt = float(data[5])
                if(latB == 0):
                    invalid = True
                params = {'scriptID': scriptID, 'flightID': flightID, 'time': int(time.time()), 'lat': latB, 'lon': lonB, 'alt':alt, 'rssi': data[6]}
                try:
                    r = requests.post(url = postURL, data = params)
                    print(r.text)
                except:
                    print("no server")
                invalid = False
            
            else:
                print("No data")
                time.sleep(1)
            
        except:
            print("bad String")
            
    print(line)
 
        