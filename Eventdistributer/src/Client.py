import json
import socket
from Loader import Loader
from Connector import Connection
from Listener import Listener
from utilities import generate_list

test = True

class Client:
    def __init__(self, host_ip):
        pi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        pi_socket.connect(("8.8.8.8", 80))
        self.pi_ip = "192.168.1.146" if test else pi_socket.getsockname()[0]
        self.reader = Loader(self.pi_ip)
        self.my_data = self.reader.get_my_config()
        self.broker_con = Connection("admin", "admin", [(host_ip, 61613)], True)
        self.my_Listener = Listener()
        self.broker_con.register_listener(self.my_Listener, "1")
        self.finished = False
        self.messages = []

    def connect_to_broker(self):
        self.broker_con.connect()

    def sub_to_topics(self):
        subscriptions = []
        for e in self.reader.get_sub():
            subscriptions.append(e["event_type"])

        for sub in subscriptions:
            self.broker_con.subscribe_to_topic(sub, self.my_data["node"])

    def pub_and_event(self, goal, data):
        pi_id, event, time_lst, value_lst, now = generate_list(goal, data)
        time_lst_str = [[date_obj.strftime("%m/%d/%Y, %H:%M:%S") for date_obj in time_lst]]
        body_content = json.dumps(
            {"pi_id": pi_id,
             "eventtype": event,
             "timestamps": time_lst_str,
             "values": value_lst,
             "timestamp": now,
             }
        )
        self.broker_con.publish_to_topic(topic=goal, message=body_content, id=pi_id)
