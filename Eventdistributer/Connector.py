import stomp
import logging

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
        self.connection= stomp.Connection(self.host_and_port)