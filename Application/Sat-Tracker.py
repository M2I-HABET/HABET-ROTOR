import math
import time
from datetime import datetime
import ephem
from urllib.request import urlopen
import scipy.constants



degrees_per_radian = 180.0 / math.pi
home = ephem.Observer()
home.lon = '-93.65338786489195'   # +E
home.lat = '42.02700680709537'      # +N
home.elevation = 80 # meters
freq = 437.550
# Always get the latest ISS TLE data from:
# http://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/orbit/ISS/SVPOST.html

url="http://www.celestrak.com/NORAD/elements/stations.txt"
req = urlopen(url)
data = req.read()

tle = data.split(b'\r\n')[0:3]
print(tle)
line1 = tle[0].decode("utf-8")
line2 = tle[1].decode("utf-8")
line3 = tle[2].decode("utf-8")

print(str(line1))
iss = ephem.readtle(line1,line2,line3)

while True:
    home.date = datetime.utcnow()
    iss.compute(home)
    print('iss: altitude %4.1f deg, azimuth %5.1f deg' % (iss.alt * degrees_per_radian, iss.az * degrees_per_radian))
    print("range velocity: "+str(iss.range_velocity))
    doplar = iss.range_velocity/scipy.constants.c*freq
    new_freq = freq+doplar
    print("new freq="+str(new_freq))
    time.sleep(1.0)