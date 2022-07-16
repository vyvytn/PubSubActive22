import json
import socket
import pathlib


class Loader():

    def __init__(self, sock):
        # setup socket and get own ip
        self.sock = sock
        sock.connect(("8.8.8.8", 80))  # ist das hier relevant?
        self.own_ip = sock.getsockname()[0]
        with open("./../resources/example_plan.json", "r") as f:
            self.data = json.load(f)

    def get_ip(self):
        return self.own_ip

    def get_sub_by_ip(self):
        pis = self.data['pis']
        pi_data = {}
        for item in pis:
            if self.own_ip == item['id']:
                pub_config = item['sub']
                return pub_config
        return {}

    def get_pub_by_id(self):
        pis = self.data['pis']
        pi_data = {}
        for item in pis:
            if self.own_ip == item['id']:
                pub_config = item['pub']
                return pub_config
        return {}

    def get_my_config(self):
        pis = self.data['pis']
        pi_data = {}
        for item in pis:
            if self.own_ip == item['id']:
                pi_data = {
                    "ip": item['id'],
                    "port": item['port'],
                    "pub": item['pub'],
                    "sub": item['sub']
                }
                return pi_data
        return {}
