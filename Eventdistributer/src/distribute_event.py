from Connector import Connection
from Listener import Listener
import json

# read json
with open("../network-plan.json", "r") as f:
    file_plan = json.load(f)

pis = []
for i in file_plan:
    pis.append(i)

for data in file_plan['pi_list']:
    print(data)


broker_con = Connection('admin', 'admin', [('127.0.0.1', 61613)], True)

broker_con.register_listener(Listener, 'listenerToTopic')

broker_con.connect()

broker_con.subscribe_to_topic('myTestTopic')

for i in range(0, 10000, 1):
    broker_con.publish_to_topic('myTestTopic', ' testing')
