from mure.dee import DistEventEmitter
import os, json, time
from gevent import sleep, spawn

dbus = DistEventEmitter()

def msg_listener(msg):
    print "received message: %s" % msg

def main():
    dbus.on('/workers/delicious', msg_listener)

if __name__ == "__main__":
    main()
