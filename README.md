### Mure
Simplified actor concurrency DSL for python
Mure stands for swarm in japanese.

### Depends on
gevent for evented I/O
kombu for transport abstraction
pybonjour for automatic configuration

### Examples
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

### More examples
    Check examples/ dir, run slacker.py in a terminal and play around

### Why ?
    This is an compilation of the same code I've been using at different projects.
    Basically it's an actor framework. Can't get easier than that.

### Future
pybonjour, otp interface, restmq transport, cluster status

