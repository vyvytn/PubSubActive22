import json


class Loader:

    def __init__(self, ip_adress):

        with open("./../resources/distribution_plan.json", "r") as f:
            self.data = json.load(f)
        self.own_ip = ip_adress

    def get_sub_by_ip(self):
        pis = self.data['pis']
        pi_data = {}
        for item in pis:
            if self.own_ip == item['ip']:
                pub_config = item['sub']
                return pub_config
        return pi_data

    def get_pub_by_ip(self):
        pis = self.data['pis']
        pi_data = {}
        for item in pis:
            if self.own_ip == item['ip']:
                pub_config = item['pub']
                return pub_config
        return pi_data

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
        return pi_data
