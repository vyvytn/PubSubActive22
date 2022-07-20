from asyncio import events
from multiprocessing.connection import wait
import time

from pkg_resources import PathMetadata

from Connector import Connection
from Listener import Listener
import json
import socket
from utils.Loader import Loader
from Client import Client
import numpy as np
import pandas as pd

import time
from Connector import Connection
import json
import random
from datetime import datetime, timedelta


pd.set_option("display.max_columns", None)

#     pub_combined_events(data, recieved_events)

def generate_list(goal, data):
    #event = "AND(C.E.B.D.F)"
    timelist = []
    values = ""
    pi_id = ""
    event_name = event
    time_now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    # print(data)
    if (
        event == "A"
        or event == "B"
        or event == "C"
        or event == "D"
        or event == "E"
        or event == "F"
    ):
        timelist.append(gen_datetime())
        values = [item for item in data["events"] if item["event_type"] == event]
        print()
    if event == "AND(C.E.B.D.F)":
        for i in range(5):
            timelist.append(gen_datetime())
        values = [e for e in data["events"] if e["event_type"] == event]
        pis = ["0", "1", "2", "3", "4", "5"]
        pi_id = random.choice(pis)

    if event == "AND(C.E.D.F)":
        for i in range(4):
            timelist.append(gen_datetime())
        values = [e for e in data["events"] if e["event_type"] == event]
        pis = ["2", "4"]
        pi_id = random.choice(pis)
    return pi_id, event_name, timelist, values, time_now


def pub_and_event(goal, data):
    print("TYPE GOAL: ", goal, type(goal))
    pi_id, event, time_lst, value_lst, now = generate_list(goal, data)

    time_lst_str = [[date_obj.strftime("%m/%d/%Y, %H:%M:%S") for date_obj in time_lst]]
    body_content = json.dumps(
        {
            "pi_id": pi_id,
            "eventtype": event,
            "timestamps": time_lst_str,
            "values": value_lst,
            "timestamp": now,
        }
    )

    my_pi.broker_con.publish_to_topic(topic=goal, message=body_content, id=pi_id)
    print("generated event FOR 'AND': ", goal)


def test_for_patternmatch_and(pattern, event, received_events):
    print(type(received_events))
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
        )
        with open("./../resources/EventTree.json", "r") as f:
            goal = "AND(C.E.B.D.F)"
            data = json.load(f)
            pub_and_event(goal, data)   
        return []
    else:
        return received_events


def test_for_patternmatch_seq(pattern, event, df_received_events):
    # print("recieved: ", received_events)
    # df_received_events = pd.DataFrame(
    #     received_events, columns=["eventtype", "timestamp"]
    # )

    if (
        len(df_received_events) == 0
        or not df_received_events["eventtype"].str.contains(event["eventtype"]).any()
    ):
        df_received_events = pd.concat([df_received_events, pd.DataFrame(event)])
    else:
        # print("element already in pattern pool")
        return df_received_events

    sorted_df = df_received_events.sort_values("timestamp")
    if (
        len(df_received_events) > 1
        and (pattern[0] == sorted_df["eventtype"].iloc[0])
        and (pattern[1] == sorted_df["eventtype"].iloc[1])
    ):
        if len(pattern) == 2:
            print("publish event SEQUENCE", sorted_df["eventtype"])
            return pd.DataFrame()
        elif (
            len(pattern) == 3
            and len(df_received_events) > 2
            and (pattern[2] == sorted_df["eventtype"].iloc[2])
        ):
            print("publish event SEQUENCE", sorted_df["eventtype"])
            return pd.DataFrame()
        else:
            return df_received_events
    else:
        return df_received_events


def test_for_patternmatch_complex_seq(pattern, event, received_events):
    df_recieved_events = pd.DataFrame(received_events)
    df_event = pd.DataFrame(event)

    # check was already recongnised:
    if (
        len(df_recieved_events) == 0
        or not df_recieved_events["eventtype"]
        .str.contains(df_event["eventtype"].iloc[0])
        .any()  # TODO some warning about extract. Nice to have level
    ):
        df_recieved_events = pd.concat([df_recieved_events, df_event])
    else:
        return received_events

    if len(df_recieved_events) > 1:
        df_recieved_events = df_recieved_events.set_index("eventtype")
        df_values = pd.DataFrame(df_recieved_events.loc["AND(E.SEQ(J.A))", "values"])
        df_values = pd.DataFrame(df_values["event_values"])

        test_time = pd.DataFrame(
            df_recieved_events.loc["AND(E.SEQ(J.A))", "timestamps"],
            columns=["timestamp"],
        )

        df_value_timestamp = pd.concat([df_values["event_values"], test_time], axis=1)
        if (
            df_recieved_events.loc["C", "timestamp"]
            < df_value_timestamp["timestamp"].iloc[1]
        ):
            print("publish event SEQUENCE", pattern)
            return pd.DataFrame()
    else:
        return df_recieved_events


my_pi = Client("127.0.0.1")
my_pi.connect_to_broker()
my_pi.sub_to_topics()
print("my_pi.reader.get_pub() ",my_pi.reader.get_pub())
messages_parsed = []

# for sequence initialise a Dataframe, and for AND an array
needed_events1 = ["B", "AND(C.E.D.F)"]
detected_events_for_pub1 = []

needed_events2 = ["AND(E.SEQ(J.A))", "C"]
detected_events_for_pub2 = pd.DataFrame()


needed_events3 = ["C", "B"]
detected_events_for_pub3 = pd.DataFrame()

needed_events4 = ["C", "B", "AND(C.E.D.F)"]
detected_events_for_pub4 = pd.DataFrame()
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

            if event["eventtype"] in needed_events3:
                detected_events_for_pub3 = test_for_patternmatch_seq(
                    needed_events3, event, detected_events_for_pub3
                )

            if event["eventtype"] in needed_events4:
                detected_events_for_pub4 = test_for_patternmatch_seq(
                    needed_events4, event, detected_events_for_pub4
                )
    i += 1
