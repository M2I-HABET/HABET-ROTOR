import math

home_lat = 42.02700680709537
home_lon = -93.65338786489195
home_alt = 350
R = 6372.795477598*1000
latA = home_lat
lonA = home_lon

latB = float(input("Lat: "))
lonB = float(input("Lon: "))
alt = float(input("Alt: "))





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