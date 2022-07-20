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

pd.set_option("display.max_columns", None)


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
        print(
            "publish event AND", plain_recieved
        )  # hier bitte publish methode ranbauen Emma, in recieved events sind alle daten der teil events
        return []
    else:
        return received_events


"""currently only works for complex events with 2 elements"""


def test_for_patternmatch_seq(pattern, event, received_events):
    print("in test for patternmatch SEQUENCE")
    test = pd.DataFrame(received_events)
    print()
    print("Dataframe:")
    print(test)

    if len(test) == 0 or event not in test:
        test = pd.concat([test, pd.DataFrame(event)])
    else:
        print("element already in pattern pool")
        return received_events
    # print("in test method SEQEUNCE ", test)

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

    if (
        len(received_events) > 1
        and (pattern[0] == sorted_df["eventtype"].iloc[0])
        and (pattern[1] == sorted_df["eventtype"].iloc[1])
    ):
        print("publish event SEQUENCE", sorted_df["eventtype"])
        return []
    else:
        return test


def test_for_patternmatch_complex_seq(pattern, event, received_events):
    print("in test for patternmatch COMPLEX SEQUENCE")
    df_recieved_events = pd.DataFrame(received_events)
    df_event = pd.DataFrame(event)
    if (
        len(df_recieved_events) == 0
        or not df_recieved_events["eventtype"]
        .str.contains(df_event["eventtype"].iloc[0])
        .any()  # TODO some warning about extract. Nice to have level
    ):
        print("eventtype not in recieved events")
        df_recieved_events = pd.concat([df_recieved_events, df_event])
    else:
        print("element already in pattern pool")
        return received_events

    if len(df_recieved_events) > 1:
        print("Dataframe of all events so far:")
        print(df_recieved_events)
        df_recieved_events = df_recieved_events.set_index("eventtype")
        print()

        df_values = pd.DataFrame(df_recieved_events.loc["AND(E.SEQ(J.A))", "values"])
        df_values = pd.DataFrame(df_values["event_values"])

        test_time = pd.DataFrame(
            df_recieved_events.loc["AND(E.SEQ(J.A))", "timestamps"],
            columns=["timestamp"],
        )

        df_value_timestamp = pd.concat([df_values["event_values"], test_time], axis=1)

        print("\n Value and Timestamp", df_value_timestamp.head())

        j_arrival_time = df_value_timestamp["timestamp"].iloc[1]
        c_arrival_time = df_recieved_events.loc["C", "timestamp"]
        print(
            "Time of C is ", c_arrival_time, "\Arrival time of j is: ", j_arrival_time
        )

        print(
            "Result of prelimenary comparison: ",
            df_recieved_events.loc["C", "timestamp"] < j_arrival_time,
        )
        if c_arrival_time < j_arrival_time:
            print("publish event SEQUENCE", pattern)
            return []
    else:
        return df_recieved_events


my_pi = Client("127.0.0.1")
my_pi.connect_to_broker()
my_pi.sub_to_topics()
messages_parsed = []
needed_events1 = ["B", "AND(C.E.D.F)"]  # emma: das sind die Teil events
detected_events_for_pub1 = []

needed_events2 = ["AND(E.SEQ(J.A))", "C"]
detected_events_for_pub2 = []

i = 0
while i in range(100):
    time.sleep(2)
    # for i in range(20):
    # my_pi.pub_to_topics()
    if len(my_pi.my_Listener.msg_list) > 0:
        event = json.loads(my_pi.my_Listener.msg_list[-1])
        if len(messages_parsed) == 0 or (messages_parsed[-1] != event):
            messages_parsed.append(event)
            if (
                event["eventtype"] in needed_events1
            ):  # in diesem if wird die and funktion aufgerufen
                detected_events_for_pub1 = test_for_patternmatch_and(
                    needed_events1, event, detected_events_for_pub1
                )
            if event["eventtype"] in needed_events2:
                detected_events_for_pub2 = test_for_patternmatch_complex_seq(
                    needed_events2, event, detected_events_for_pub2
                )

    print(len(messages_parsed))
    i += 1
