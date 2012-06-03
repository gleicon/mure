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
        dbus.emit("message", "hnam %d" % count) 
        sleep(5)

def join_listener(msg):
    print "%s" % msg

def msg_listener(msg):
    print "received message: %s" % msg

def main():
    dbus.emit('join', "oeam")
    dbus.on('messages', msg_listener)
    producer()

if __name__ == "__main__":
    main()
