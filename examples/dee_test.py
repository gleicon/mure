from mure.dee import DistEventEmitter
import os, json, time
from gevent import sleep, spawn

dbus = DistEventEmitter()

def producer():
    count =0
    while(True):
        count = count +1
        print count
        dbus.emit("message", "hnam %d" % count) 
        sleep(5)

def join_listener(msg):
    print "%s" % msg

def msg_listener(msg):
    print "received message: %s" % msg

def main():
    dbus.emit('join', "oeam")
    dbus.on('/workers/delicious', msg_listener)
    producer()

if __name__ == "__main__":
    main()
