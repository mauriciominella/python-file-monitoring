from multiprocessing import Process
from subprocess import call
import time
import os
from datetime import datetime

def read_data(outputFile):
    f = open(outputFile, "w")
    for i in range(10):
        call(['sleep', '3']) 
        call(['echo', str(i)], stdout=f) 


def do_task(outputFile):
    task = Process(target=read_data, args=(outputFile,))
    task.start()
    while True:
        time.sleep(1)
        modificationDate = modification_date(outputFile)
        secondsSinceLastWrite = (datetime.now() - modificationDate).total_seconds()
        fileSize = os.path.getsize(outputFile)
        if secondsSinceLastWrite > 10:
            return 
        else :
            yield fileSize, secondsSinceLastWrite, task

    task.join()


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t)


if __name__ == '__main__':
    outputFile = "blah.txt"
    for fileSize, secondsSinceLastWrite, task in do_task(outputFile):
       print fileSize, secondsSinceLastWrite, task 
       if fileSize > 5:
           print 'file size limit exceeded, finish him!'
           task.terminate()

    print 'done!'
