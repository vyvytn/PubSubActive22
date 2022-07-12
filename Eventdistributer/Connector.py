import stomp
import logging
import Listener
log= logging.getLogger('Connector.py')

class Singleton(type):
    def __init__(cls, name, bases, dic):
        super(Singleton, cls).__init__(name, bases, dic)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)

        return cls.instance

class Connection(stomp.Connection):
    __metaclass__= Singleton

    def __init__(self, username, password, host_port, wait=True):
        self.username=username
        self.password=password
        self.host_port= host_port
        self.wait=wait
        self.stomp_con= stomp.Connection(self.host_and_port)
    
    def register_listener(self, listener):
        self.stomp_con.set_listener(listener, Listener())

    def connect(self):
        self.stomp_con.start()
        self.stomp_con.connect(self.username, self.password, self.wait)

    def subscribe_to_topic(self, topic):
        self.stomp_con.subscribe(destination=topic, id='1', ack='auto')

    def publish_to_topic(self, topic, message):
        self.stomp_con.send(destination=topic, body=message)
   
    def disconnect(self):
            self.stomp_con.disconnect()
