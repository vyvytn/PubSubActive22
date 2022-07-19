from asyncio import events
from multiprocessing.connection import wait
import time

from Connector import Connection
from Listener import Listener
import json
import socket
from utils.Loader import Loader
from Client import Client
import numpy as np
import pandas as pd


def test_for_patternmatch_and(pattern, event, received_events):
    plain_recieved = []
    for e in received_events:
        plain_recieved.append(e["eventtype"])
    if event["eventtype"] not in plain_recieved:
        received_events.append(event)
        plain_recieved.append(event["eventtype"])
    else:
        return received_events
    if np.in1d(pattern, plain_recieved).all():
        print("publish event AND", plain_recieved)
        return []
    else:
        return received_events


def test_for_patternmatch_seq(pattern, event, received_events):
    print("in test for patternmatch SEQUENCE")
    plain_recieved = []
    for e in received_events:
        plain_recieved.append(e["eventtype"])
    print("Recieved Events", received_events)
    if event["eventtype"] not in plain_recieved:
        print("in method eventtepye not in recieved events")
        received_events.append(event)
        plain_recieved.append(event["eventtype"])
    else:
        print("returned ealry")
        return received_events
    print("in test method SEQEUNCE ", received_events)
    test = pd.DataFrame(received_events)
    print()
    print("Dataframe:")
    print(test)

    print()
    print("Dataframesorted:")
    sorted_df = test.sort_values("timestamps")
    print(sorted_df)

    print()

    print("equal check prep")

    print(
        "is the first element of the pattern ( ",
        pattern[0],
        " ) and the observed sequence ( ",
        sorted_df["eventtype"].iloc[0],
        " equal? ",
        pattern[0] == sorted_df["eventtype"].iloc[0],
    )

    if len(received_events) > 1 and (pattern[0] == sorted_df["eventtype"].iloc[0]):
        print("publish event SEQUENCE", plain_recieved)
        return []
    else:
        return received_events


my_pi = Client("127.0.0.1")
my_pi.connect_to_broker()
my_pi.sub_to_topics()
messages_parsed = []
needed_events1 = ["B", "AND(C.E.D.F)"]
detected_events_for_pub1 = []
# needed_events2 = ["C", "AND(E.SEQ(J.A))"]
needed_events2 = ["C", "B"]
detected_events_for_pub2 = []
# print(my_pi.reader.get_pub())
i = 0
while i in range(100):
    time.sleep(2)
    # for i in range(20):
    # my_pi.pub_to_topics()
    if len(my_pi.my_Listener.msg_list) > 0:
        event = json.loads(my_pi.my_Listener.msg_list[-1])
        if len(messages_parsed) == 0 or (messages_parsed[-1] != event):
            messages_parsed.append(event)
            if event["eventtype"] in needed_events1:
                detected_events_for_pub1 = test_for_patternmatch_and(
                    needed_events1, event, detected_events_for_pub1
                )
            if event["eventtype"] in needed_events2:
                detected_events_for_pub2 = test_for_patternmatch_seq(
                    needed_events2, event, detected_events_for_pub2
                )

            # if (
            #     event["eventtype"] == "AND(C.E.D.F)"
            #     and "AND(C.E.D.F)" in needed_events1
            #     and event["eventtype"] not in needed_events1
            # ):
            #     generated_event1.append(event)
            #     generated_event1 = test_for_patternmatch_and_cebdf(generated_event1)

    # print("messages_parsed: ", messages_parsed)
    # print("outside for ", messages_parsed)
    print(len(messages_parsed))
    i += 1
