# Distributed Event Emitter inspired by pyee
from __future__ import with_statement
from collections import defaultdict
from kombu import BrokerConnection
import os, json
import gevent
from gevent import monkey
from Queue import Empty

monkey.patch_all()

class DistEventEmitter:
    def __init__(self, transport_url = "redis://127.0.0.1:6379", timeout = 60):
        self._events = defaultdict(lambda:[])
        self._event_watchers = defaultdict(lambda:[])
        self._transport_url = transport_url
        self._id = "node:%d" % os.getpid()
        self._timeout = timeout

    def _watcher(self, event):
        with BrokerConnection(self._transport_url) as conn:
            with conn.SimpleQueue(event) as queue:
                while True:
                    try:
                        message = queue.get(block=True, timeout=10)
                        if message:
                            self._emit(event, message.payload)
                            message.ack()
                    except Empty:
                        pass

    def _broadcast(self, event, message):
        with BrokerConnection(self._transport_url) as conn:
            with conn.SimpleQueue(event) as queue:
                queue.put(message)

    def on(self, event, fun):
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
        self._events[event].remove(fun)
        gevent.kill(self._event_watchers[event])

    def remove_all_listeners(self, event):
        self._events[event] = []

    def once(self, event, fun):
        def _onetime(f, *args, **kwargs):
            def g(*args, **kwargs):
                f(*args, **kwargs)
                self.remove_listener(event, g)
            return g
        self.on(event, _onetime(fun))

