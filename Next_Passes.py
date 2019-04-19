import math
import ephem
from urllib.request import urlopen
from datetime import date, datetime, timezone

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

obs = ephem.Observer()
obs.lat = '42.02700680709537'
obs.long = '-93.65338786489195'

for p in range(3):
    print("Set:"+str(p))
    tr, azr, tt, altt, ts, azs = obs.next_pass(iss)
    tr1 = tr
    tr = tr.datetime()
    tr = tr.replace(tzinfo=timezone.utc).astimezone(tz=None)
    ts = ts.datetime()
    ts = ts.replace(tzinfo=timezone.utc).astimezone(tz=None)
    print("Start Date: %s \nStart Time: %s \nMax Altitude: %2.1f \nSet Time %s" % (tr.date(), tr.time(), ephem.degrees(altt)*180/math.pi, ts.time()))
    obs.date = tr1 + 40 * ephem.minute
