from multiprocessing import Process
from subprocess import call
import time
import os
from datetime import datetime

FILE_SIZE_LIMIT_IN_BYTES = 1000
LAST_CHANGE_ELAPSED_TIME_LIMIT = 10

def write_data(outputFile):
    f = open(outputFile, "w")
    for i in range(10):
        call(['sleep', '3']) 
        call(['echo', 'writing file...' + str(i)], stdout=f) 


def do_task(outputFile):
    task = Process(target=write_data, args=(outputFile,))
    task.start()
    while True:
        time.sleep(1)
        modificationDate = modification_date(outputFile)
        secondsSinceLastWrite = (datetime.now() - modificationDate).total_seconds()
        fileSizeInBytes = os.path.getsize(outputFile)
        stillProcessing = task.is_alive()
        yield fileSizeInBytes, secondsSinceLastWrite, stillProcessing, task

    # print 'finalizou'
    # task.join()


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t)


if __name__ == '__main__':
    outputFile = "blah.txt"
    for fileSizeInBytes, secondsSinceLastWrite, stillProcessing, task in do_task(outputFile):
        print fileSizeInBytes, secondsSinceLastWrite, stillProcessing, task 
        if not stillProcessing:
            print 'process is done!'
            break

        if secondsSinceLastWrite > LAST_CHANGE_ELAPSED_TIME_LIMIT:
            print 'too long without writing anything'
            break 

        if fileSizeInBytes > FILE_SIZE_LIMIT_IN_BYTES:
           print 'file size limit exceeded, finish him!'
           task.terminate()
           break

    print " process is alive? R={alive}".format(alive=task.is_alive())

    # if anything goes wrong, wait for the process to finish
    task.join()

    print 'done!'
