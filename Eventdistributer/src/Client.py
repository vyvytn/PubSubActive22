from datetime import datetime
import socket
from utils.Loader import Loader
from Connector import Connection
from Listener import Listener


def create_body(content):
    message = {
        'timestamps': [],
        'values': [],
        'pi_id': '',
        'event_name': 'event',
        'time_now': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    }
    return message


def and_operator(self, content):
    pass


def seq_operator(self, content):
    pass


class Client:

    def __init__(self, host_ip):
        pi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        pi_socket.connect(("8.8.8.8", 80))  # ist das hier relevant?
        self.pi_ip = pi_socket.getsockname()[0]
        self.reader = Loader(self.pi_ip)
        self.my_data = self.reader.get_my_config()
        self.broker_con = Connection('admin', 'admin', [(host_ip, 61613)], True)

    def connect_to_broker(self):
        self.broker_con.register_listener(Listener, 'listenerToTopic')
        self.broker_con.connect()

    def sub_to_topics(self):
        for sub in self.my_data['sub']:
            self.broker_con.subscribe_to_topic(sub, self.my_data['node'])

    def pub_to_topics(self):
        print(self.my_data['pub'])
        for topic in self.my_data['pub']:
            pass
