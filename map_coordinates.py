# Install Mapping software
import tilemapbase
# Pandas (for fun)
import pandas as pd
#Import needed libraries, mainly numpy, matplotlib and basemap
import math
import numpy as np
import matplotlib.pyplot as plt
# Import the Image function from the IPython.display module.
from IPython.display import Image
import time
import multiprocessing
import multiprocessing.managers
import logging

"""
This is the local flight plotter for HABET flights.  This uses tilemapbase and should be 

It will grab new data every 5 seconds and add it to the GPS data lists.  Every 15 seconds, it 
will plot a new flight path 
"""

logger = multiprocessing.log_to_stderr()
logger.setLevel(logging.INFO)


class MyListManager(multiprocessing.managers.BaseManager):
    pass

MyListManager.register("syncarr")

def main(): 
    manager = MyListManager(address=('/tmp/mypipe'), authkey=''.encode('utf-8')) # this is for UNIX
    # manager = MyListManager(address=('192.168.1.205', 8080), authkey=''.encode('utf-8'))
    manager.connect()
    syncarr = manager.syncarr()

    # initialize lists to hold our GPS data 
    lat = []
    lon = []
    alt = []
    change_size = False
    max_lat = 0
    min_lat = 0
    max_lon = 0
    min_lon = 0

    i = 0

    test_data = []

    # For testing purposes
    # gps = open("HABET-ROTOR/datalog.txt", "r")
    # gps = open("HABET-ROTOR/flight_path_2021_08_13.csv")
    # for line in gps :
    #     test_data.append(line.split(","))
    #     # lat.append(float(splitline[1])/10000000.0)
    #     # lon.append(float(splitline[2])/10000000.0)
    #     # alt.append(float(splitline[3])/1000.0)
    # gps.close()
    # Initialize the tilemapbase
    tilemapbase.init(create=True)

    # Coordinates for launch sites 
    howe_hall = (-93.65287451738621, 42.027034639829346) # other flights use this
    four_H = (-93.55537888198775, 41.592104221317534) # use this for the state fair flight

    launch_site = howe_hall

    # Add the initial coordinates to the longitude and latitude lists
    lon.append(launch_site[0])
    lat.append(launch_site[1])
    min_lon = launch_site[0]
    max_lon = launch_site[0]
    min_lat = launch_site[1]
    max_lat = launch_site[1]

    # Get the range for what the tilemapbase should be looking for (I think?)
    degree_range = 0.25
    extent = tilemapbase.Extent.from_lonlat(launch_site[0] - degree_range, launch_site[0] + degree_range,
                    launch_site[1] - degree_range, launch_site[1] + degree_range)
    extent = extent.to_aspect(1.0)

    # Convert to web mercator
    path = [tilemapbase.project(x,y) for x,y in zip(lon, lat)]
    x, y = zip(*path)
    fig, ax = plt.subplots()
    plotter = tilemapbase.Plotter(extent, tilemapbase.tiles.build_OSM(), width=600)

    # Plot and then save to a JPG which will then be used to display the balloon's path
    plotter.plot(ax)
    ax.plot(x, y,"b-")
    plt.axis('off')
    plt.savefig('HABET-ROTOR/map.jpg',bbox_inches = "tight",dpi = 300)
    time.sleep(1)
    plt.close()

    while 1:
        print("===MAP GPS DATA===")
        valid = True
        while valid :
            print("Getting data for mapping flight path")
            try: 
                print("Getting data for mapping flight path")
                test_string = ""
                data = syncarr
                latB = float(data[1])/10000000
                lonB = float(data[2])/10000000
                # latB = float(gps_data[1])
                # lonB = float(gps_data[2])
                if latB > max_lat :
                    max_lat = latB
                    change_size = True
                elif latB < min_lat :
                    min_lat = latB
                    change_size = True
                if lonB > max_lon :
                    max_lon = lonB
                    change_size = True
                elif lonB < min_lon :
                    min_lon = lonB
                    change_size = True
                print("lat: ", latB)
                print("lon: ", lonB)
                lat.append(latB)
                lon.append(lonB)
                valid = False
                if i == 0 :
                    """To make sure that the map will be large enough to view where we are at
                    get the maximum and minimum of the data points and use that to get the 
                    extent of the map
                    """
                    # max_lon = max(lon)
                    # min_lon = min(lon)
                    # max_lat = max(lat)
                    # min_lat = min(lat)

                    # Plot the values 
                    print("plotting values!")
                    if change_size :
                        extent = tilemapbase.Extent.from_lonlat(min_lon - degree_range, max_lon + degree_range,
                        min_lat - degree_range, max_lat + degree_range)
                        extent = extent.to_aspect(1.0)
                        change_size = False
                    # Convert to web mercator
                    path = [tilemapbase.project(x,y) for x,y in zip(lon, lat)]
                    x, y = zip(*path)
                    fig, ax = plt.subplots()
                    plotter = tilemapbase.Plotter(extent, tilemapbase.tiles.build_OSM(), width=600)
                    plotter.plot(ax)
                    ax.plot(x, y,"b-")
                    plt.axis('off')
                    plt.savefig('HABET-ROTOR/map.jpg',bbox_inches = "tight",dpi = 300)
                    time.sleep(1)
                    plt.close()
                    print("Saved picture!")
            except :

                print("syncarr may not be set, or no new data")
                continue
            else :
                time.sleep(1)
        time.sleep(5)
        i = (i+1)%15


if __name__ == '__main__':
    main()

# Coordinates of fair are: 
# lon_4h = 41.592104221317534 
# lat_4h = -93.55537888198775

