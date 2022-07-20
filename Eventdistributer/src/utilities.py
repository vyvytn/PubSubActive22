from datetime import datetime, timedelta
import json
import random
import numpy as np
import pandas as pd


def gen_datetime(min_year=2022, max_year=datetime.now().year):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()


def open_pub(pi, goal=""):
    with open("./../resources/EventTree.json", "r") as f:
        data = json.load(f)
        pi.pub_and_event(goal, data)


# generates an event object with its timestamp and tree of events
def generate_list(event, data):
    timelist = []
    values = ""
    pi_id = ""
    time_now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
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
    if event == "SEQ(J.A)":
        for i in range(2):
            timelist.append(datetime.now() + timedelta(seconds=i))
        values = [e for e in data["events"] if e["event_type"] == event]
        pi_id = "4"
    if event == "SEQ(A.F.C)":
        for i in range(3):
            timelist.append(datetime.now() + timedelta(seconds=i))
        values = [e for e in data["events"] if e["event_type"] == event]
        pi_id = "0"
    if event == "AND(C.E.D.F)":
        for i in range(4):
            timelist.append(gen_datetime())
        values = [e for e in data["events"] if e["event_type"] == event]
        pis = ["2", "4"]
        pi_id = random.choice(pis)
    if event == "AND(C.E.B.D.F)":
        for i in range(5):
            timelist.append(gen_datetime())
        values = [e for e in data["events"] if e["event_type"] == event]
        pis = ["0", "1", "2", "3", "4", "5"]
        pi_id = random.choice(pis)
    if event == "AND(E.SEQ(C.J.A)":
        for i in range(2):
            timelist.append(datetime.now() + timedelta(seconds=i))
        values = [e for e in data["events"] if e["event_type"] == event]
        pis = ["5", "9"]
        pi_id = random.choice(pis)
    if event == "AND(E.SEQ(J.A)":
        for i in range(2):
            timelist.append(datetime.now() + timedelta(seconds=i))
        values = [e for e in data["events"] if e["event_type"] == event]
        pi_id = "9"

    return pi_id, event, timelist, values, time_now


# matched incoming complex AND-events
# pi - brokerclient, goal - event tp be published, pattern - subscribed events for goal, event - incoming eventtype, received_events - all relevent events since last matched
def test_for_patternmatch_and(pi, goal, pattern, event, received_events):
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
        open_pub(pi, goal)
        return []
    else:
        return received_events


# matched incoming complex SEQ-events
# pi - brokerclient, goal - not exist because of mocking, pattern - subscribed events for goal, event - incoming eventtype, received_events - all relevent events since last matched
def test_for_patternmatch_seq(pi, pattern, event, df_received_events):
    if (
        len(df_received_events) == 0
        or not df_received_events["eventtype"].str.contains(event["eventtype"]).any()
    ):
        df_received_events = pd.concat([df_received_events, pd.DataFrame(event)])
    else:
        return df_received_events
    sorted_df = df_received_events.sort_values("timestamp")
    if (
        len(df_received_events) > 1
        and (pattern[0] == sorted_df["eventtype"].iloc[0])
        and (pattern[1] == sorted_df["eventtype"].iloc[1])
    ):
        if len(pattern) == 2:
            print("\n publish event SEQUENCE for: \n", sorted_df["eventtype"])
            open_pub(pi)
            return pd.DataFrame()
        elif (
            len(pattern) == 3
            and len(df_received_events) > 2
            and (pattern[2] == sorted_df["eventtype"].iloc[2])
        ):
            print("\n publish event SEQUENCE for: \n", sorted_df["eventtype"])
            open_pub(pi)
            return pd.DataFrame()
        else:
            return df_received_events
    else:
        return df_received_events


# matched incoming complex AND-events
# pi - brokerclient, goal - event tp be published, pattern - subscribed events for goal, event - incoming eventtype, received_events - all relevent events since last matched
def test_for_patternmatch_complex_seq(pi, goal, pattern, event, received_events):
    df_recieved_events = pd.DataFrame(received_events)
    df_event = pd.DataFrame(event)
    # check was already recongnised:
    if (
        len(df_recieved_events) == 0
        or not df_recieved_events["eventtype"]
        .str.contains(df_event["eventtype"].iloc[0])
        .any()
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
            open_pub(pi, goal)
            return pd.DataFrame()
    else:
        return df_recieved_events
