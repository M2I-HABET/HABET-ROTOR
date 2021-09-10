import math
import time
from datetime import datetime
import ephem
from urllib.request import urlopen
import scipy.constants
import subprocess
import rot2proG

degrees_per_radian = 180.0 / math.pi
home = ephem.Observer()
home.lon = '-93.65338786489195'   # +E
home.lat = '42.02700680709537'      # +N
home.elevation = 300  # meters
freq = 145.825 * 10 ** 6
radio_com = "COM9" #this may be the correct com port for the penthouse - mjk 2021-07-05
radio_baud = "9600"
radio_model = "101"  # hamlib radio model number
rotor_com = "COM5" #this may be the correct com port for the penthouse - mjk 2021-07-05

url = "http://www.celestrak.com/NORAD/elements/stations.txt"
req = urlopen(url)
data = req.read()

tle = data.split(b'\r\n')[0:3]
print(tle)
line1 = tle[0].decode("utf-8")
line2 = tle[1].decode("utf-8")
line3 = tle[2].decode("utf-8")

print(str(line1))
iss = ephem.readtle(line1, line2, line3)
rot = rot2proG.Rot2proG(rotor_com)
numberOfruns = 0
while True:
    home.date = datetime.utcnow()
    iss.compute(home)
    print('iss: altitude %4.1f deg, azimuth %5.1f deg' %
          (iss.alt * degrees_per_radian, iss.az * degrees_per_radian))
    print("range velocity: "+str(iss.range_velocity))
    doplar = iss.range_velocity/scipy.constants.c*freq
    new_freq = freq+doplar
    if(iss.alt * degrees_per_radian > 0):
        print("new freq="+str(new_freq))
        subprocess.call(["rigctl", "-r", radio_com, "-s",
                         radio_baud, "-m", radio_model, "F", str(new_freq)])
        print("Satalite over head. Moving...")
        rot.set(int(iss.az * degrees_per_radian),
                int(iss.alt * degrees_per_radian))
    else:
        print("moving az")
        
        rot.set(int(iss.az * degrees_per_radian),
                int(0))
    stat = rot.status()
    print("current rot pos: az=%3.0f el=%2.0f" % (stat[0], stat[1]))
    time.sleep(10)
    numberOfruns = numberOfruns + 1
    print()
    if numberOfruns == 1000:
        numberOfruns = 0
        print("Updating the TLE")
        req = urlopen(url)
        data = req.read()

        tle = data.split(b'\r\n')[0:3]
        print(tle)
        line1 = tle[0].decode("utf-8")
        line2 = tle[1].decode("utf-8")
        line3 = tle[2].decode("utf-8")
        print(str(line1))
        iss = ephem.readtle(line1, line2, line3)
