import rot2proG
import serial
import math
import time

home_lat = 42.02700680709537
home_lon = -93.65338786489195
home_alt = 300
R = 6372.795477598*1000

latA = home_lat
lonA = home_lon
run = True
vCom = serial.Serial(port="COM21", baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=None)
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
        if vCom.in_waiting:
            line = vCom.readline()
        time.sleep(.1)
        if line != "":
            invalid = False
            data = line.decode("utf-8").strip("\n").split(",")[0:3]
            latB = float(data[0])#43.02700680709
            lonB = float(data[1])#-94.6533878648
            alt = float(data[2])
            if(latB == 0):
                invalid = True
        else:
            print("No data")
    print(line)
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
        dla = latA-latB
        dlo = lonA-lonB
        print(dla)
        print(dlo)
        if((dla>0 and dlo<0) or (dla>0 and dlo>0) ):
            az = az + 180
            if(az<170):
                az = az+180
        if((dla<0 and dlo>0)):
            az = az + 360
        el = math.atan(int(alt-home_alt)/distance)
        print("el")
        print(el)
        print("az")
        print(az)
        print("distance;")
        print(distance)
        if(el<0):
            el = 0
        
        time.sleep(.1)
        run = True
        rot.set(az,el)
    except:
        e = sys.exc_info()[0]
        print(e)
        