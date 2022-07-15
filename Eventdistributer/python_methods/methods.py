import socket
import json
import pathlib


def main():
	# example to test eventdata
	datastream = ["c,a,f,c,f,g,k,e,b,d"]


    #read json
	with open(str(pathlib.Path(__file__).parent.resolve()) + "/network-plan.json", "r") as f:
		config = json.load(f)[own_ip]

	# read event operators and types
	for i in config["pub"] :
	    operator = config["pub"][i]["event_operator"]
	    event = config["pub"][i]["eventtype"][0]
	    receiving = config["pub"][i]["recieveing_brokers"]
	    
	    if operator == "seq":
	        broker_list = []
	        print("seq: ", event)
	        if event in datastream[0]:
	            print("occurence of '", event, "' found")
	            for j in receiving:
	                print ("new broker found: ", j)
	                broker_list = broker_list + [j]
	            print(broker_list)
	            # pub event to broker_list
	   

	    if operator == "plain":
	        broker_list = []
	        print("plain: ", event)

	        if event in datastream[0]:
	            print("occurence of '", event, "' found")
	            for j in receiving:
	                print ("new broker found: ", j)
	                broker_list = broker_list + [j]
	            print(broker_list)
	            # pub event to broker_list


	    if operator == "and":
	        broker_list = []
	        print("and: ", event, event[0], event[1] == ",")
	        event = event.split(",")
	        length = 0
	        exists = 0
	        for j in event:
	            print(j, type(event))
	            length = length +1 
	            if j in datastream [0]:
	                exists = exists +1
	        if length == exists:
	            print("occurence of '",operator, event, "' found")
	            for j in receiving:
	                print ("new broker found: ", j)
	                broker_list = broker_list + [j]
	            print(broker_list)
	            
	            # then pub event to broker_list
	            


