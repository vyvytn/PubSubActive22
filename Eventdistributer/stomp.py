import stomp
import time
import sys

def connect_and_subscribe(conn):
    conn.connect('guest', 'guest', wait=True)
    conn.subscribe(destination='/queue/test', id=1, ack='auto')

class Listener(stomp.ConnectionListener):   
    
    def __init__(self, conn):
        self.conn = conn

    def on_error(self, frame):
        print('received an error "%s"' % frame.body)

    def on_message(self, frame):
        print('received a message "%s"' % frame.body)
        for x in range(10):
            print(x)
            time.sleep(1)
        print('processed message')

    def on_disconnected(self):
        print('disconnected')
        connect_and_subscribe(self.conn)

conn = stomp.Connection([('localhost',8161)])
print('set up Connection')

lstn= Listener()
conn.set_listener('somename', lstn)
print('Set up listener')

conn.start()
print('started connection')

conn.connect('admin', 'admin', wait=True)
print('connected')

conn.subscribe(destination='/queue/test', id=1, ack='auto')
print('subscribed')

message='hello cruel world'
conn.send(message= message, destination='/queue/test')
print('sent message')
time.sleep(2)
print('slept')
conn.disconnect()
print('disconnected')
"""conn = stomp.Connection()
lst = MyListener()
conn.set_listener('', lst)
conn.start()
conn.connect()
conn.subscribe(destination='/queue/test', id=1, ack='auto')
time.sleep(2)
messages = lst.msg_list
conn.disconnect()
return render(request, 'template.html', {'messages': messages})"""