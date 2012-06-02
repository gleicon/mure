from __future__ import with_statement
from kombu.common import maybe_declare
from kombu.pools import producers
from kombu import BrokerConnection, Exchange, Queue
from kombu.pools import connections


"""
shows how to send a message from kombu to a given worker
useful to integrage to existing code
let slackers.py running in a different shell
"""

transport_url = "redis://127.0.0.1:6379"
connection = BrokerConnection(transport_url)
_queue = "/workers/delicious"
_queue2 = "/workers/jazz"
qname1 = Queue(_queue, Exchange("exchange:%s" % _queue, type='fanout'))
qname2 = Queue(_queue2, Exchange("exchange:%s" % _queue2, type='fanout'))

if __name__ == "__main__":
    with connections[connection].acquire(block=True) as conn:
        with conn.SimpleQueue(qname1) as queue:
            queue.put("mensagem")
    
    with connections[connection].acquire(block=True) as conn:
        with conn.SimpleQueue(qname2) as queue:
            queue.put("mensagem2")


