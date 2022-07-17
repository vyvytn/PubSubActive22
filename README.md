# Event disributer with a Pub/Sub model

Using activemq and stomp protocol in python.

## Project structure

 - Event distributer: Project directory
     - resources: event distribution plan
     - utils: supporting methods and libraries
     - src: source code
       - Client: Every Pi is a client with an unique id and an ip adress. Within the class all information about this pi is stored. A connection to the broker will be established and the distribution plan as the input will be parsed.
       - Connector: Establishes a connection to the broker as a stomp client.
       - Listener: This class extends the stomp Connection Listener class and hence it overrides the some of the
    methods of the same as per the minimal usage . This is default listener class which will inject for the connection
    with stomp if no other listener is passed.
       - RandomEventGenerator: Publishes randomly events with messages.
       - distribute_event: Main method for each pi. Executes 
	 
## Getting started
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

4. Navigate now to the project folder and execute RandomEventGenerator.py for simulating events and distribute_event.py for event detection and evaluation:
```
python RandomEventGenerator.py distribute_event.py
```
