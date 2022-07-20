import time
from Connector import Connection
import json
import random
from datetime import datetime, timedelta

host_adress = "127.0.0.1"

# create the order of the test set you want to publish here. Events will be created in pubevents.
test = [
    "C",
    "B",
    "AND(C.E.D.F)",
    "J",
    "A",
    "A",
    "F",
    "C" "C",
    "B",
    "A",
    "AND(E.SEQ(J.A))",
    "B",
    "AND(C.E.D.F)",
    "A",
    "B",
    "C",
    "A",
    "E",
    "D",
    "F",
    "A",
    "F",
    "J",
]

# start iteration at 0
j = 0


def gen_datetime(min_year=2022, max_year=datetime.now().year):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()


def generate_list(event, data):
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
    if event == "AND(E.SEQ(C.J.A))":
        for i in range(2):
            timelist.append(datetime.now() + timedelta(seconds=i))
            values = [e for e in data["events"] if e["event_type"] == event]
            pis = ["5", "9"]
            pi_id = random.choice(pis)
            if event == "AND(E.SEQ(J.A))":
                for i in range(2):
                    timelist.append(datetime.now() + timedelta(seconds=i))
                    values = [e for e in data["events"] if e["event_type"] == event]
                    pi_id = "9"
    if event == "AND(E.SEQ(J.A))":
        for i in range(2):
            timelist.append(
                datetime.now() + timedelta(seconds=40) + timedelta(seconds=i)
            )
            values = [e for e in data["events"] if e["event_type"] == event]
        pi_id = "9"
    return pi_id, event_name, timelist, values, time_now


def pub_events(data, test):
    broker_con = Connection("admin", "admin", [(host_adress, 61613)], True)
    broker_con.connect()
    global j
    evt = test[j]
    j = j + 1
    pi_id, event, time_lst, value_lst, now = generate_list(evt, data)
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

    broker_con.publish_to_topic(topic=evt, message=body_content, id=pi_id)
    print("generated event ", evt)


with open("./../resources/EventTree.json", "r") as f:
    data = json.load(f)
    while j < len(test):
        pub_events(data, test)
        time.sleep(4)
