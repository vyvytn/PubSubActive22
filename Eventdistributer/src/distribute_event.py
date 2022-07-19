import time

from Connector import Connection
from Listener import Listener
import json
import socket
from utils.Loader import Loader
from Client import Client

my_pi = Client("127.0.0.1")
my_pi.connect_to_broker()
my_pi.sub_to_topics()

# while True:
for i in range(20):
    my_pi.pub_to_topics()
