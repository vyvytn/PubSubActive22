import json
import socket
import pathlib


#setup socket and get own ip
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("8.8.8.8", 80)) # ist das hier relevant?
own_ip = sock.getsockname()[0]
print('Current IP adress is: ',own_ip)

#read json
with open(str(pathlib.Path(__file__).parent.resolve()) + "/network-plan.json", "r") as f:
    config = json.load(f)[own_ip]


subscriptions= config["sub"]
publishes = config["pub"]
brokernumber= config["id_from_queryformat"]
#print('Broker ', brokernumber, ' subscribes to ', subscriptions, ' and publishes ', publishes)
#print(publishes[0][0])
print(config["pub"]["1"]["event_operator"])
