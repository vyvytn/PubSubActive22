from msilib import sequence


datastream = ["c", "a", "f", "c", "f", "g", "k", "e", "f", "a", "c", "b", "d"]
event_operator = "seq"
event_type = ["a", "f", "c"]


sequence_iterator = 0
for e in datastream:
    if e == event_type[sequence_iterator]:
        print(sequence_iterator, " sequence element matched:", e)
        if sequence_iterator == len(event_type) - 1:
            print("full seq matched")
            sequence_iterator = 0
        else:
            sequence_iterator += 1
