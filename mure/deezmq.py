# Distributed Event Emitter inspired by pyee using zmq and pub/sub pgm sockets
# over multicast

from collections import defaultdict
import os, json
import gevent
from gevent import monkey
import zmq

monkey.patch_all()

class DistEventEmitter:
    def __init__(self, transport_url = "epgm://225.0.0.73:12345", timeout = 60):
        self._events = defaultdict(lambda:[])
        self._event_watchers = defaultdict(lambda:[])
        self._transport_url = transport_url
        self._id = "node:%d" % os.getpid()
        self._timeout = timeout

        self._pub_context = zmq.Context()
        self._pub_socket = self._pub_context.socket(zmq.PUB)
        self._pub_socket.connect(self._transport_url)
        
        self._sub_context = zmq.Context()
        self._sub_socket = self._sub_context.socket(zmq.SUB) 
        self._sub_socket.connect(self._transport_url)

    def _watcher(self, event):
        while True:
            try:
                message = self._sub_socket.recv()
                if message:
                    self._emit(event, message.payload)
            except Exception, e:
                print e

    def _broadcast(self, event, message):
        try:
            self._pub_socket.send(message)
        except Exception, e:
            print e
    
    def on(self, event, fun):
        self._sub_socket.setsockopt(zmq.SUBSCRIBE, event)
        self._events[event].append(fun)
        self._event_watchers[event].append(gevent.spawn(self._watcher, event))
        
    def emit(self, event, message):
        packed_msg = json.dumps({'_id': self._id, 'message': message})
        self._emit(event, packed_msg)
        self._broadcast(event, packed_msg)

    def _emit(self, event, message):
        m = json.loads(message)
        if m['_id'] == self._id: return
        for f in self._events[event]:
            f(message)

    def listeners(self, event):
        return self._events[event]

    def remove_listener(self, event, fun):
        self._sub_socket.setsockopt(zmq.UNSUBSCRIBE, event)
        self._events[event].remove(fun)
        gevent.kill(self._event_watchers[event])

    def remove_all_listeners(self, event):
        for e in self._events[event]:
            self._sub_socket.setsockopt(zmq.UNSUBSCRIBE, event)
        self._events[event] = []

    def once(self, event, fun):
        def _onetime(f, *args, **kwargs):
            def g(*args, **kwargs):
                f(*args, **kwargs)
                self.remove_listener(event, g)
            return g
        self.on(event, _onetime(fun))

