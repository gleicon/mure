### Mure
Simplified actor concurrency DSL for python. Includes a distributed EventEmitter
Mure stands for swarm in japanese.

### Depends on
gevent for evented I/O
kombu for transport abstraction
pybonjour for automatic configuration

### Actor Example
    from mure.core import worker, send_message, connect, disconnect

    @worker('awesomenator')
    def be_awesome(message):
        send_message('call_me_whenever_awesome_is_ready', 'awesomenator is being awesome, message: %s' % message)

    @worker('call_me_whenever_awesome_is_ready')
    def omg_awesome(message):
        print 'seems like someone was awesome: %s ' % message

    if __name__ == "__main__":
        from time import sleep
        connect()
        sleep(10)
        disconnect()

from python, ipython or bpython:

    from mure.core import send_message, connect, disconnect
    connect()
    send_message('awesomenator', 'release the kraken')
    disconnect()

### Distributed Event Emitter example
It works as node.js EventEmitters, inspired by pyee (https://github.com/jesusabdullah/pyee).
The same syntax applies, it packs the message as json, with a node id.
Internally it avoids feedbacking the message back to the original sender.
Run this example in different terminals

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
        dbus.on('message', msg_listener)
        producer()

    if __name__ == "__main__":
        main()

### node.js binding

    If you are using kombu + redis there is a binding on node.js/ dir that reproduces its protocol on a kind of distributed event emitter. 
    Basically it is a 2 or more channel redis based kombu port for node.js integrated to EventEmitter.  

On node.js
    
    var dee = require("./dee")
    dee = dee.create_dee();                                                         
    dee.worker("/workers/jazz", function(w) { console.log(w) });                    
    dee.send_message("/workers/delicious", "wot");

On Python

    from mure.dee import DistEventEmitter
    dbus = DistEventEmitter()

    def msg_listener(msg): 
        print "received message: %s" % msg                                          
                                                                                
    def main():
        dbus.on('/workers/delicious', msg_listener)    

    if __name__ == "__main__":
        main()

    Run examples/dee_test.py in a term and then node.js/test.js to check the communication. This example is a self-counting event emitter with message exchange between two processes. To the original intent redis support is enough (just cheap signaling to a node.js process that could lose a step)

### More examples
    Check examples/ dir, run slacker.py in a terminal and play around

### Why ?
    This is an compilation of the same code I've been using at different projects.
    Basically it's an actor framework. Can't get easier than that.

### Future
pybonjour, otp interface, restmq transport, cluster status, node.js/ruby library

