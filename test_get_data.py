import time

import multiprocessing
import multiprocessing.managers

import logging
logger = multiprocessing.log_to_stderr()
logger.setLevel(logging.INFO)


class MyListManager(multiprocessing.managers.BaseManager):
    pass

MyListManager.register("syncarr")

def main(): 
   

    # def main():
    # manager = MyListManager(address=('/tmp/mypipe'), authkey=''.encode('utf-8'))
    manager = MyListManager(address=('192.168.1.205', 8080), authkey=''.encode('utf-8'))
    manager.connect()
    syncarr = manager.syncarr()

    print ("arr = %s" % (dir(syncarr)))

    # note here we need not bother with __str__ 
    # syncarr can be printed as a list without a problem:
    print ("List at start:", syncarr)
    print ("Changing from client")
    # syncarr.append(30)
    # print ("List now:", syncarr)

    o0 = None
    o1 = None

    while 1:
        valid = True
        while valid :
            try: 
                test_string = ""
                data = syncarr
                latB = float(data[1])/10000000
                lonB = float(data[2])/10000000
                alt = float(data[3])/1000
                print("lat: ", latB)
                print("lon: ", lonB)
                print("alt: ", alt)
                valid = False
            except :
                print("syncarr may not be set, or no new data")
                continue
            finally:
                time.sleep(1)


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