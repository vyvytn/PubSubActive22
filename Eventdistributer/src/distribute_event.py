from Connector import Connection
from Listener import Listener
import json
import socket
from utils.Loader import Loader

pi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
pi_socket.connect(("8.8.8.8", 80))  # ist das hier relevant?
pi_ip = pi_socket.getsockname()[0]

# read json
reader = Loader(socket.AF_INET, socket.SOCK_DGRAM)

my_data = reader.get_my_config()
print(my_data)
broker_con = Connection('admin', 'admin', [('127.0.0.1', 61613)], True)

broker_con.register_listener(Listener, 'listenerToTopic')

broker_con.connect()

for sub in my_data['sub']:
    broker_con.subscribe_to_topic(sub, my_data['node'])
