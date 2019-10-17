import rot2proG
import serial
import math
import time
import requests
import json

home_lat = 42.02700680709537
home_lon = -93.65338786489195
home_alt = 300
R = 6372.795477598*1000

flightID = "a8fa88c0-a1b2-4751-a3e9-44a7419b0983"
scriptID = "429c4f46-140b-4db4-8cf9-6acc88f5b019"
postURL = "http://127.0.0.1:8000/REST/V1/flight_location"
aprsURL = "http://api.aprs.fi/api/get?name=W0ISU-10&what=loc&apikey=128630.PDyTBXmisXvARO&format=json"
run = True

while run:
    line = ""
    invalid = True
    print("start while")
    data = ""
    latB = ''
    lonB = ''
    alt = ''
    try:
        vals = requests.post(url = aprsURL)
        jsonVals = json.loads(vals.text)
        print(jsonVals['entries'])
        latB = float(jsonVals['entries'][0]['lat'])#43.02700680709
        lonB = float(jsonVals['entries'][0]['lng'])#-94.6533878648
        alt = float(jsonVals['entries'][0]['altitude'])
    
    except:
        print("no dat")
        time.sleep(2)
        continue
    print(latB)
    print(lonB)
    print(alt)
    
    if(latB != 0):
        invalid = True
        params = {'scriptID': scriptID, 'flightID': flightID, 'time': int(time.time()), 'lat': latB, 'lon': lonB, 'alt':alt, 'rssi': 0}
        try:
            r = requests.post(url = postURL, data = params)
            print(r.text)
        except:
            print("no server")
        invalid = False
    time.sleep(60)
            

 
        