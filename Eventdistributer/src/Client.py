from ast import Load
import json
import time
from datetime import datetime
import socket
from utils.Loader import Loader
from Connector import Connection
from Listener import Listener
import numpy as np

test = True


def create_body(content):
    message = {
        "timestamps": [],
        "values": [],
        "pi_id": "",
        "event_name": "event",
        "time_now": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
    }
    return message





def and_operator(self, sub, query, messages, timelist=None):
    published_events = [e["event_type"] for e in query]
    subscribed_events = [e["event_type"] for e in sub]
    goal_number = []
    needed_events1 = []
    needed_events2 = []
    generated_event1 = []
    generated_event2 = []
    incoming_events = []
    messages_parsed = []
    for e in query:
        goal_number.append(len(e["event_values"]))
        # needed_events.append([event["event_type"] for event in e["event_values"]])
        # needed_events[0]
    if query[0]["event_type"] == "AND(C.E.B.D.F)":
        needed_events1 = ["B", "AND(C.E.D.F)"]
    if query[0]["event_type"] == "AND(E.SEQ(C.J.A))":
        needed_events2 = ["C", "AND(E.SEQ(J.A))"]

    test_int = 0
    while test_int < 10:
        print("while loop round ", test_int)
        messages_parsed = []
        for m in messages:
            messages_parsed.append(json.loads(m))
        print("messages_parsed: ", messages_parsed)
        incoming_events = [m for m in messages_parsed]
        for event in incoming_events:
            print("eventtype", event["eventtype"])

            if event["eventtype"] == "B":
                if "B" in needed_events1 and event not in generated_event1:
                    generated_event1.append(event)
                    generated_event1 = test_for_patternmatch_and_cebdf(generated_event1)

            if (
                event["eventtype"] == "AND(C.E.D.F)"
                and "AND(C.E.D.F)" in needed_events1
                and event["eventtype"] not in needed_events1
            ):
                generated_event1.append(event)
                generated_event1 = test_for_patternmatch_and_cebdf(generated_event1)

            # if event["eventtype"] == "C" and "C" in needed_events2:
            #     generated_event2.append(event)
            #     needed_events2.remove(event["eventtype"])

            # if (
            #     event["eventtype"] == "AND(E.SEQ(J.A)"
            #     and "AND(E.SEQ(J.A)" in needed_events2
            # ):
            #     generated_event2.append(event)
            #     needed_events2.remove(event["eventtype"])

            incoming_events.remove(event)

        test_int += 1
    # return generated_event


def seq_operator(self, sub, query, messages):
    sequence_iterator = 0
    # messages ['{"pi_id": "4", "eventtype": "AND(CEDF)", "timestamps": ["11/23/2022, 06:51:47", "07/12/2022, 15:41:12", "11/17/2022, 22:04:30", "09/13/2022, 10:31:09"], "values": ["C", "E", "D", "F"], "timestamp": "07/17/2022, 15:49:36"}', '{"pi_id": "2", "eventtype": "AND(CEDF)", "timestamps": ["09/20/2022, 13:12:19", "02/09/2022, 01:31:51", "06/10/2022, 09:52:30", "08/28/2022, 23:49:33"], "values": ["C", "E", "D", "F"], "timestamp": "07/17/2022, 15:49:39"}', '{"pi_id": "4", "eventtype": "AND(CEDF)", "timestamps": ["03/06/2022, 10:17:32", "12/12/2022, 12:15:31", "07/16/2022, 18:05:17", "08/06/2022, 03:22:17"], "values": ["C", "E", "D", "F"], "timestamp": "07/17/2022, 15:49:42"}', '{"pi_id": "2", "eventtype": "AND(CEDF)", "timestamps": ["09/01/2022, 07:43:28", "06/08/2022, 04:57:19", "10/01/2022, 15:45:27", "10/06/2022, 18:01:24"], "values": ["C", "E", "D", "F"], "timestamp": "07/17/2022, 15:49:45"}']
    for e in messages:
        if e["eventtype"] == query:
            print("SAME SAME")
        """if e == event_type[sequence_iterator]:
            print(sequence_iterator, " sequence element matched:", e)
            if sequence_iterator == len(event_type) - 1:
                print("full seq matched")
                sequence_iterator = 0
            else:
                sequence_iterator += 1"""


class Client:
    def __init__(self, host_ip):
        pi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        pi_socket.connect(("8.8.8.8", 80))  # ist das hier relevant?
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

    def pub_to_topics(self):
        self.finished = False
        needed_events1 = []
        needed_events2 = []
        generated_event1 = []
        generated_event2 = []
        incoming_events = []
        messages_parsed = []

        needed_events1 = ["B", "AND(C.E.D.F)"]

        needed_events2 = ["C", "AND(E.SEQ(J.A))"]

        for event in messages_parsed:
            print("eventtype", event["eventtype"])

            if event["eventtype"] == "B":
                if "B" in needed_events1 and event not in generated_event1:
                    generated_event1.append(event)
                    generated_event1 = test_for_patternmatch_and_cebdf(generated_event1)

            if (
                event["eventtype"] == "AND(C.E.D.F)"
                and "AND(C.E.D.F)" in needed_events1
                and event["eventtype"] not in needed_events1
            ):
                generated_event1.append(event)
                generated_event1 = test_for_patternmatch_and_cebdf(generated_event1)

            # if event["eventtype"] == "C" and "C" in needed_events2:
            #     generated_event2.append(event)
            #     needed_events2.remove(event["eventtype"])

            # if (
            #     event["eventtype"] == "AND(E.SEQ(J.A)"
            #     and "AND(E.SEQ(J.A)" in needed_events2
            # ):
            #     generated_event2.append(event)
            #     needed_events2.remove(event["eventtype"])

            incoming_events.remove(event)
