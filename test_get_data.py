import time

import multiprocessing
import multiprocessing.managers

import logging
logger = multiprocessing.log_to_stderr()
logger.setLevel(logging.INFO)


class MyListManager(multiprocessing.managers.BaseManager):
    pass

MyListManager.register("syncarr")

# def main():
manager = MyListManager(address=('/tmp/mypipe'), authkey=''.encode('utf-8'))
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
    test_string = ""
    for item in syncarr :
        test_string += item
    
    print(test_string)
    time.sleep(1)


# if __name__ == '__main__':
#     main()