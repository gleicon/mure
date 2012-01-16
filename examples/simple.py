import sys, os
sys.path.append("..")
sys.path.append(os.path.join(sys.path[0], '..'))

from mure.core import connect, disconnect, worker, send_message
from time import sleep

@worker('/workers/delicious')
def a_worker(message):
    print "received: %s" % message
    send_message('/workers/jazz', 'd-d-d-dance')

@worker('/workers/jazz')
def another_worker(message):
    print "received2: %s" % message
    send_message('/workers/delicious', "saaaap")

@worker('/workers/delicious')
def third_worker(message):
    print "the other worker received: %s" % message

if __name__ == "__main__":
    connect() 
    send_message('/workers/jazz', 'let it start')
    sleep(1)
    disconnect()
