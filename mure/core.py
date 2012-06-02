from __future__ import with_statement
from kombu import BrokerConnection, Exchange, Queue
from collections import defaultdict
import gevent
from gevent import monkey
monkey.patch_all()

class WorkerHub():
    """
    WorkerHub controls the local mailboxes that the @worker decorator assigns.
    Also contains a method to send messages to given workers
    Depends on kombu + gevent, uses SimpleQueue. default transport is redis
    """
    def __init__(self, transport_url = "redis://127.0.0.1:6379"):
        self.workers = defaultdict(set)
        self._transport_url = transport_url
        self._connected = False
    
    def add_worker(self, workername, callback):
        self.workers[workername].add(callback)
        def _listener():
            qname = Queue(workername, Exchange("exchange:%s" % workername, type='fanout'))
            while self._connected == False:
                print "waiting %s" % self._connected
                gevent.sleep(1)
            with BrokerConnection(self._transport_url) as conn:
                with conn.SimpleQueue(qname) as queue:
                    while True:
                        try:
                            message = queue.get(block=True, timeout=10)
                            if message:
                                self._execute_callbacks(workername, message.payload)
                                message.ack()
                                if self._connected == False: break
                        except:
                            pass
        gevent.spawn(_listener)

    def _execute_callbacks(self, workername, message):
        for w in self.workers[workername]:
            w(message)

    def send_message(self, workername, message):
        if self._connected == False: return
        qname = Queue(workername, Exchange("exchange:%s" % workername, type='fanout'))
        with BrokerConnection(self._transport_url) as conn:
            with conn.SimpleQueue(qname) as queue:
                queue.put(message)

    def connect(self, transport_url=None):
        self._connected = True
        print "connected: %s" % self._connected
        if transport_url: self._transport_url = transport_url

    def disconnect(self):
        self._connected = False

wh = WorkerHub()

def connect(transport_url = None):
    """
    start all workers. provide a different transport url following kombu URI
    scheme.
    if no transport is given, defaults to local redis. if there are no workers, 
    connect to the cluster to enable message passing
    connect()
    """
    if transport_url is None:
        transport_url = "redis://127.0.0.1:6379"
    wh.connect(transport_url)

def disconnect():
    """
    disconnect and stop all workers.
    """
    wh.disconnect()

def worker(workername):
    """
    gevent/kombu based worker
    prepend this decorator to a function that might receive the message.
    broadcasts the message to all callbacks appended.
    ex:
    @worker("/queue")
    def my_processor(message):
        print message

    """
    def _decorator(f):
        wh.add_worker(workername, f)
        return f
    return _decorator

def send_message(workername, message):
    """
    send a message to a given worker, using the same key as the worker
    decorator.
    send_message("/queue", "my message")
    """
    wh.send_message(workername, message)

