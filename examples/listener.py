import sys, os
sys.path.append("..")
sys.path.append(os.path.join(sys.path[0], '..'))

from mure.core import connect, disconnect, worker, send_message
from time import sleep

@worker('/workers/delicious')
def a_worker(message):
    print "received: %s" % message

@worker('/workers/jazz')
def another_worker(message):
    print "received2: %s" % message

@worker('/workers/delicious')
def third_worker(message):
    print "the other worker received: %s" % message

if __name__ == "__main__":
    connect() 
    sleep(1000)
    disconnect()
