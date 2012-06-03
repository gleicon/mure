import os, json, time, sys
from gevent import sleep, spawn
sys.path.append("..")                                                           
from mure.deezmq import DistEventEmitter

dbus = DistEventEmitter(transport_url = "tcp://127.0.0.1:1111")

def producer():
    count =0
    while(True):
        count = count +1
        print count
        dbus.emit("messages", "hnam %d" % count) 
        sleep(2)

def main():
    producer()

if __name__ == "__main__":
    main()
