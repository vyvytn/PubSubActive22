import time
import sys
import logging
import stomp
from stomp import ConnectionListener

queuename = sys.argv[1]

logging.basicConfig( level=logging.DEBUG)

class MyListener(ConnectionListener):
    def on_error(self, headers, message):
        print 'received an error %s' % message

    def onMessage(self, headers, message):
        print headers
        print str(message)
        print type(message)
        print 'received a message ...%s...' % message


conn = stomp.Connection([('localhost', 61613)])                                                                                               
conn.set_listener('', MyListener())
conn.start()
conn.connect()


conn.subscribe(destination='/queue/'+queuename, ack='auto')


while 1:
    time.sleep(2)