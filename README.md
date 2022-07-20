# Event disributer with a Pub/Sub model

Using activemq and stomp protocol in python.

## Project structure

 - Event distributer: Project directory
     - resources: event distribution plan
     - src: source code
       - Client: Every Pi is a client with an unique id and an ip adress. Within the class all information about this pi is stored. A connection to the broker will be established and the distribution plan as the input will be parsed.
       - Connector: Establishes a connection to the broker as a stomp client.
       - Listener: This class extends the stomp Connection Listener class and hence it overrides the some of the
    methods of the same as per the minimal usage . This is default listener class which will inject for the connection
    with stomp if no other listener is passed.
       - TestEventGenerator: Publishes randomly events with messages.
       - distribute_event: Main method for each pi. Executes 
	 
## Getting started
0. Might need to install the newest version of pandas and numpy
1. get active mq e.g. with shell:
```
wget http://archive.apache.org/dist/activemq/activemq-artemis/2.23.1/
```
2. unzip it:
```
tar zxvf apache-activemq-2.23.1-bin.tar.gz  
```
3. Navigate to the bin directory of active mq and start it:
```
./activemq start 
```

4. Navigate now to the project folder and execute RandomEventGenerator.py for simulating events and distribute_event.py for event detection and evaluation. This needs to happen in to different shells, as the pocesses need to be parallel, if the functionality is tested locally.

```
python RandomEventGenerator.py 
python distribute_event.py
```

## Currently enabled example:
The current host adress is coded into TestEventGenerator.py and distribute_event.py, this might need to be adjusted.
As coded in distributed_event.py the current script creates a client, similar node 5 in the queryformat.py, that subscribes to the topics:
- "B"
- "AND(C.E.D.F)"
- "AND(E.SEQ(J.A))"
- "C"

and publishes:
- AND(E.SEQ(C.J.A))
- AND(C.E.B.D.F)

It also recognizes 2 more complex event type to show the implemented functionality also works sequence. However, this can only be observed as a print() statement, and is not published to apache. 

### Test Event Sequence
Currently the sequence of events is mock-published as shown in TextEventGenerator.py



