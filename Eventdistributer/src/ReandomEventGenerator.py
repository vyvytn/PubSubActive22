import time
from Connector import Connection
import json
import random
from datetime import datetime, timedelta

local = '127.0.0.1'


def gen_datetime(min_year=2022, max_year=datetime.now().year):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()


def generate_list(event):
    timelist = []
    values = []
    pi_id = ''
    event_name = event
    time_now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    if event == 'A' or event == 'B' or event == 'C' or event == 'D' or event == 'E' or event == 'F':
        timelist.append(gen_datetime())
        values.append(event)
    if event == 'SEQ(JA)':
        for i in range(2):
            timelist.append(datetime.now() + timedelta(seconds=i))
        values.append('J')
        values.append('A')
        pi_id = '4'
    if event == 'SEQ(AFC)':
        for i in range(3):
            timelist.append(datetime.now() + timedelta(seconds=i))
        values.append('A')
        values.append('F')
        values.append('C')
        pi_id = '0'
    if event == 'AND(CEDF)':
        for i in range(4):
            timelist.append(gen_datetime())
        values.append('C')
        values.append('E')
        values.append('D')
        values.append('F')
        pis = ['2', '4']
        pi_id = random.choice(pis)
    if event == 'AND(CEBDF)':
        for i in range(5):
            timelist.append(gen_datetime())
        values.append('C')
        values.append('E')
        values.append('B')
        values.append('D')
        values.append('F')
        pis = ['0', '1', '2', '3', '4', '5']
        pi_id = random.choice(pis)
    if event == 'AND(E,SEQ(CJA)':
        for i in range(4):
            timelist.append(datetime.now() + timedelta(seconds=i))
        values.append('E')
        values.append('C')
        values.append('J')
        values.append('A')
        pis = ['5', '9']
        pi_id = random.choice(pis)
    if event == 'AND(E,SEQ(JA)':
        for i in range(3):
            timelist.append(gen_datetime())
        values.append('E')
        values.append('J')
        values.append('A')
        pi_id = '9'
    return pi_id, event_name, timelist, values, time_now


def pub_events():
    broker_con = Connection('admin', 'admin', [(local, 61613)], True)
    broker_con.connect()
    """event_types = ['A', 'B', 'C', 'D', 'E', 'F', 'SEQ(AFC)', 'SEQ(JA)', 'AND(CEDF)', 'AND(CEBDF)', 'AND(ESEQ(CJA)',
                   'AND(ESEQ(JA)']"""
    event_types = ['B', 'AND(CEDF)']
    evt = random.choice(event_types)
    pi_id, event, time_lst, value_lst, now = generate_list(evt)
    time_lst_str = [date_obj.strftime("%m/%d/%Y, %H:%M:%S") for date_obj in time_lst]
    body_content = json.dumps([pi_id, event, time_lst_str, value_lst, now])
    broker_con.publish_to_topic(topic=evt, message=body_content, id=pi_id)


for i in range(10000):
    pub_events()
    time.sleep(3)
