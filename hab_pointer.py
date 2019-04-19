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

while run:
    line = ""
    while ser.in_waiting:  # Or: while ser.inWaiting():
        line = ser.readline()
        time.sleep(1)
    print(data)
    data = line.split(",")[0:3]
    latB = data[0]#43.02700680709
    lonB = data[1]#-94.6533878648
    alt = data[1]
    distance = R * math.acos (math.pi/180*math.sin(latA) * math.sin(math.pi/180*latB) + math.cos(math.pi/180*latA) * math.cos(math.pi/180*latB) * math.cos(math.pi/180*(lonA-lonB)))

    x = math.cos(latB*math.pi/180)*math.sin(math.pi/180*(lonA-lonB))
    y = math.cos(latA*math.pi/180)*math.sin(math.pi/180*latB)-math.sin(math.pi/180*latA)*math.cos(math.pi/180*latB)*math.cos(math.pi/180*(lonA-lonB))
    
    az =  -180/math.pi*math.atan(x/y)
    dla = latA-latB
    dlo = lonA-lonB
    if((dla>0 and dlo<0) or (dla>0 and dlo>0) ):
        az = az + 180
        if(az<170):
            az = az+180
    if((dla<0 and dlo>0)):
        az = az + 360
    el = math.atan(int(alt)/distance)
    print(az)
    time.sleep(.1)
    run = False