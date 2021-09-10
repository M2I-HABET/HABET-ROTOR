import time
import multiprocessing
import multiprocessing.managers
import logging
from datetime import datetime

logger = multiprocessing.log_to_stderr()
logger.setLevel(logging.INFO)


class MyListManager(multiprocessing.managers.BaseManager):
    pass

MyListManager.register("syncarr")

def main(): 
   

    # def main():
    manager = MyListManager(address=('/tmp/mypipe'), authkey=''.encode('utf-8'))
    # manager = MyListManager(address=('192.168.1.31', 8080), authkey=''.encode('utf-8'))
    manager.connect()
    syncarr = manager.syncarr()
    max_height = 36700
    # print ("arr = %s" % (dir(syncarr)))

    # note here we need not bother with __str__ 
    # syncarr can be printed as a list without a problem:
    # print ("List at start:", syncarr)
    # syncarr.append(30)
    # print ("List now:", syncarr)
    now = None
    while 1:
        print("===DISPLAY DATA FOR OBS===")
        invalid = True
        while invalid :
            print("Getting data for OBS")
            try: 
                # Get the data
                data = syncarr
                lat = float(data[1])/10000000
                lon = float(data[2])/10000000
                alt = float(data[3])/1000
                temp = float(data[4])
                hum = float(data[5])
                pres = float(data[6])
                if max_height < alt :
                    max_height = alt
                # Save the time it was saved
                now = datetime.now()
                print("lat: ", lat)
                print("lon: ", lon)
                print("alt: ", alt)
                print
                f = open('obs_data.txt', "w")
                print("Latitude: ", lat, file=f)
                print("Longitude: ", lon, file=f)
                print("Altitude (meters): ", round(alt), "m", file=f)
                print("Altitude (feet): ", round(alt*3.281),"ft", file=f)
                print("Temperature: ", temp, "C", file=f)
                print("Humidity: ", hum, "%", file=f)
                print("Pressure: ", pres, "hPa", file=f)
                print("Max Alt: ", round(max_height),"m, ", round(max_height*3.281), "ft", file=f)
                invalid = False
                f.close()
            except :
                print("syncarr may not be set, or no new data")
                try:
                    print("Last data sent: ", now.strftime("%Y-%m-%d-%H:%M:%S"))
                except:
                    print("No last data")
                continue
            finally:
                time.sleep(5)


        # item1 = syncarr.__get_item__(1)
        # item2 = syncarr.__get_item__(2)
        # item3 = syncarr.__get_item__(3)
        # data = syncarr
        # item1 = data[1]

        
        # print(test_string)
        # print("item1: ", item1)
        # print("item2: ", item2)
        # print("item3: ", item3)
        time.sleep(1)


if __name__ == '__main__':
    main()