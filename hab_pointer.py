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

flightID = "07a8aac0-3a38-412a-a0a8-cbd5a3777d67"
postURL = "http://10.29.188.15/REST/V1/flightpos/"+flightID
latA = home_lat
lonA = home_lon
run = True
rot = rot2proG.Rot2proG("COM7")
while run:
    line = ""
    invalid = True
    print("start while")
    data = ""
    latB = ''
    lonB = ''
    alt = ''
    while invalid:  # Or: while ser.inWaiting():
        try:
            r = requests.post(url = postURL, data = {})
            print(r.text)
            json_data = json.loads(r.text)
            latB = float(json_data['lat'])#43.02700680709
            lonB = float(json_data['lon'])#-94.6533878648
            alt = float(json_data['alt'])
            invalid = False
        except:
            print("no server")
            continue
        
        
                
    try:
        
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
        #print(alt)
        #print(home_alt)
        print("elevation: "+ str(el))
        print("Azumuth: " + str(az))
        print("Distacne: "+ str(distance))
        if(el<0):
            el = 0
        
        time.sleep(2)
        run = True
        rot.set(az,el)
    except:
        e = sys.exc_info()[0]
        print(e)
        