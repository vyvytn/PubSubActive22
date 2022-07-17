import json
import socket
import pathlib


class Loader():

    def __init__(self, sock1, sock2):
        # setup socket and get own ip
        sock = socket.socket(sock1, sock2)
        sock.connect(("8.8.8.8", 80))  # ist das hier relevant?
        self.own_ip = sock.getsockname()[0]
        with open("./../resources/distribution_plan.json", "r") as f:
            self.data = json.load(f)

    def get_ip(self):
        return self.own_ip

    def get_sub_by_ip(self):
        pis = self.data['pis']
        pi_data = {}
        for item in pis:
            if self.own_ip == item['ip']:
                pub_config = item['sub']
                return pub_config
        return {}

    def get_pub_by_ip(self):
        pis = self.data['pis']
        pi_data = {}
        for item in pis:
            if self.own_ip == item['ip']:
                pub_config = item['pub']
                return pub_config
        return {}

    def get_my_config(self):
        pis = self.data['pis']
        pi_data = {}
        for item in pis:
            if self.own_ip == item['ip']:
                pi_data = {
                    "ip": item['ip'],
                    "node": item['node_id'],
                    "pi_name": item['pi_id'],
                    "pub": item['pub'],
                    "sub": item['sub']
                }
                return pi_data
        return {}
