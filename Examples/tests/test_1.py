import stomp
from stomp import *

conn  = Connection([('127.0.0.1', 61613)])

conn.connect('admin', 'password', wait=True)
conn.set_listener('', PrintingListener())
conn.subscribe('/topic/test', 123)#unique subscription id
conn.send(body='A', destination='/topic/Topic_A')
conn.send(body='BBBBBBBAAAAAAAABAAAAAAAAAA', destination='/topic/Topic_A')

conn.disconnect()
