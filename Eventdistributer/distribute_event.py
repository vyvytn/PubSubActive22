from Connector import Connection 
from Listener import Listener
broker_con= Connection('admin', 'admin', [('127.0.0.1', 61613)], True)

broker_con.register_listener(Listener, 'listenerToTopic')

broker_con.connect()

broker_con.subscribe_to_topic('myTestTopic')

for i in range(0, 10000, 1):
    broker_con.publish_to_topic('myTestTopic', ' testing')