import stomp
import logging
log = logging.getLogger('Connector.py')


class Singleton(type):
    def __init__(cls, name, bases, dic):
        super(Singleton, cls).__init__(name, bases, dic)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)

        return cls.instance


class Connection(stomp.Connection):
    __metaclass__ = Singleton

    def __init__(self, username, password, host_port, wait=True):
        self.username = username
        self.password = password
        self.host_port = host_port
        self.wait = wait
        self.stomp_con = stomp.Connection(self.host_port)

    def register_listener(self, listener_obj, listener_id):
        self.stomp_con.set_listener(listener_id, listener_obj())

    def connect(self):
        # self.stomp_con.start()
        self.stomp_con.connect(self.username, self.password, self.wait)

    def subscribe_to_topic(self, topic, id):
        self.stomp_con.subscribe(destination='/topic/'+topic, id=id, ack='auto')

    def publish_to_topic(self, topic, message):
        self.stomp_con.send(destination='/topic/'+topic, body=message)

    def disconnect(self):
        self.stomp_con.disconnect()
