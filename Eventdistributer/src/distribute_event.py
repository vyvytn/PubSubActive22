from Client import Client
import numpy as np
import pandas as pd
import time
import json
import random
from datetime import datetime, timedelta
from utilities import test_for_patternmatch_and,test_for_patternmatch_complex_seq,test_for_patternmatch_seq
pd.set_option("display.max_columns", None)

my_pi = Client("127.0.0.1")
my_pi.connect_to_broker()
my_pi.sub_to_topics()
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

goal1 =["AND(C.E.B.D.F)"]
goal2 =["AND(E.SEQ(C.J.A))"]
"""goal3 =[""]
goal4 =[""]"""
i = 0
while i in range(100):
    time.sleep(2)
    # for i in range(20):
    # my_pi.pub_to_topics()
    if len(my_pi.my_Listener.msg_list) > 0:
        event = json.loads(my_pi.my_Listener.msg_list[-1])
        if len(messages_parsed) == 0 or (messages_parsed[-1] != event):
            messages_parsed.append(event)
            if event["eventtype"] in needed_events1:  # in diesem if wird die and funktion aufgerufen
                detected_events_for_pub1 = test_for_patternmatch_and(my_pi,goal1, needed_events1,event, detected_events_for_pub1)
            if event["eventtype"] in needed_events2:
                detected_events_for_pub2 = test_for_patternmatch_complex_seq(my_pi, goal2,needed_events2, event,
                                                                             detected_events_for_pub2)

            if event["eventtype"] in needed_events3:
                detected_events_for_pub3 = test_for_patternmatch_seq(my_pi, needed_events3, event,
                                                                     detected_events_for_pub3)

            if event["eventtype"] in needed_events4:
                detected_events_for_pub4 = test_for_patternmatch_seq(my_pi, needed_events4, event,
                                                                     detected_events_for_pub4)
    i += 1
