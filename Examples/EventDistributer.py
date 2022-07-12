import os
import json
from stomp import Stomp
from stomp import StompConfig

CONFIG = StompConfig(uri=os.environ['MQ_URL'],
                     login=os.environ['MQ_UID'],
                     passcode=os.environ['MQ_DWP'],
                     version="1.2")

topic = '/topic/SAMPLE.TOPIC'

msg = {'refresh': True}

client = Stomp(CONFIG)
client.connect()
client.send(topic, json.dumps(msg).encode())
client.disconnect()

client = Stomp(CONFIG)
client.connect(heartBeats=(0, 10000))
token = client.subscribe(topic, {
    "ack": "client",
    "id": '0'
})

frame = client.receiveFrame()
if frame and frame.body:
    print(f"Frame received from MQ: {frame.info()}")
client.disconnect()