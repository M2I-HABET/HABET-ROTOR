import time
import multiprocessing
import multiprocessing.managers
import logging
from datetime import datetime

"""
This is a script that will save the data from data_broker into a text file in order to display onto an OBS Stream.
Since OBS needs a textfile that is constantly written to, the data needs to be written to a text file.
"""




logger = multiprocessing.log_to_stderr()
logger.setLevel(logging.INFO)


class MyListManager(multiprocessing.managers.BaseManager):
    pass

MyListManager.register("syncarr")

def main(): 
   

    # Attach to the data_broker script
    manager = MyListManager(address=('/tmp/mypipe'), authkey=''.encode('utf-8'))
    # manager = MyListManager(address=('192.168.1.31', 8080), authkey=''.encode('utf-8'))
    manager.connect()
    syncarr = manager.syncarr()

    # Max height variable that will update every iteration
    max_height = 0

    now = None
    # Begin the main script
    while 1:
        print("===DISPLAY DATA FOR OBS===")
        invalid = True
        while invalid :
            print("Getting data for OBS")
            try: 
                # Get the data
                data = syncarr
                # get all of the GPS and atmospheric data and convert to display
                lat = float(data[1])/10000000
                lon = float(data[2])/10000000
                alt = float(data[3])/1000
                temp = float(data[4])
                hum = float(data[5])
                pres = float(data[6])
                # if there is a new highest altitude, update it!
                if max_height < alt :
                    max_height = alt
                # Save the time it was saved
                now = datetime.now()
                print("lat: ", lat)
                print("lon: ", lon)
                print("alt: ", alt)

                # Now save the data found into a text file.  
                f = open('obs_data.txt', "w")
                print("Latitude: ", lat, file=f)
                print("Longitude: ", lon, file=f)
                print("Altitude (meters): ", round(alt), "m", file=f)
                # convert some of the data for viewers
                print("Altitude (feet): ", round(alt*3.281),"ft", file=f)
                print("Temperature: ", temp, "C", file=f)
                print("Humidity: ", hum, "%", file=f)
                print("Pressure: ", pres, "hPa", file=f)
                print("Max Alt: ", round(max_height),"m, ", round(max_height*3.281), "ft", file=f)
                invalid = False
                # make sure the file is closed so the changes can be saved
                f.close()
            except :
                # "error" messages 
                print("syncarr may not be set, or no new data")
                try:
                    print("Last data sent: ", now.strftime("%Y-%m-%d-%H:%M:%S"))
                except:
                    print("No last data")
                continue
            finally:
                # only update the numbers every 5 or so seconds
                time.sleep(5)
        time.sleep(1)

# run the script
if __name__ == '__main__':
    main()