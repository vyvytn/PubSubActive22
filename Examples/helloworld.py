import stomp
import sys
c= stomp.Connection
c.connect('admin', 'admin', wait=True)
c.send(body=' '.join(sys.argv[1:]), destination='/queue/test')
c.disconnect