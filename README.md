# Event disributer with a Pub/Sub model

Using activemq and stomp protocol in python.

## Project structure

 - Event distributer: Project directory
	 - resources: event distribution plan
	 - utils: supporting methods and libraries
	 - src: source code
	 
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

4. Navigate now to the project folder and execute distribute_event.py:
```
python distribute_event.py
```
