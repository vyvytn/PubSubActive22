import time
import logging
import stomp

log = logging.getLogger("listener.py")

"""
    This class extends the stomp Connection Listener class and hence it overrides the some of the
    methods of the same as per the minimal usage . This is default listener class which will inject for the connection
    with stomp if no other listener is passed.
"""


class Listener(stomp.PrintingListener):
    """
    Called by the STOMP connection once a TCP/IP connection to the
    STOMP server has been established or re-established.
    """

    def __init__(self):
        super().__init__()
        self.msg_list = []

    def on_connecting(self, host_and_port):
        now = int(time.time())
        log.debug(
            "STOMP connection initiated at  message server at %s  ",
            str(now) + " at host and port " + str(host_and_port),
        )
        print(
            "STOMP connection initiated at  message server at %s  ",
            str(now) + " at host and port " + str(host_and_port),
        )

    """
        Called by the STOMP connection when a CONNECTED frame is
        received
    """

    def on_connected(self, frame):
        return super().on_connected(frame)

    """Called by the STOMP connection when a TCP/IP connection to the
        STOMP server has been lost.  No messages should be sent via
        the connection until it has been reestablished."""

    def on_disconnected(self):
        return super().on_disconnected()

    """Called by the STOMP connection when a heartbeat message has not been
        received beyond the specified period."""

    def on_heartbeat_timeout(self):
        return super().on_heartbeat_timeout()

    """Called by the STOMP connection before a message is returned to the client app. Returns a tuple
        containing the headers and body (so that implementing listeners can pre-process the content).
        :param dict headers: the message headers
        :param body: the message body

    def on_before_message(self, frame):
        return super().on_before_message(frame)"""

    """ Called by the STOMP connection when a MESSAGE frame is received.
        :param dict headers: a dictionary containing all headers sent by the server as key/value pairs.
        :param body: the frame's payload - the message body.
        """

    def on_message(self, frame):
        self.msg_list.append(frame.body)
        return super().on_message(frame)

    """ Called by the STOMP connection when a RECEIPT frame is
        received, sent by the server if requested by the client using
        the 'receipt' header.
        :param dict headers: a dictionary containing all headers sent by the server as key/value pairs.
        :param body: the frame's payload. This is usually empty for RECEIPT frames."""

    def on_receipt(self, frame):
        return super().on_receipt(frame)

    """Called by the STOMP connection when an ERROR frame is received.
        :param dict headers: a dictionary containing all headers sent by the server as key/value pairs.
        :param body: the frame's payload - usually a detailed error description."""

    def on_error(self, frame):
        return super().on_error(frame)

    """Called by the STOMP connection when it is in the process of sending a message
        :param Frame frame: the frame to be sent"""

    def on_send(self, frame):
        return super().on_send(frame)

    """        Called on receipt of a heartbeat."""

    def on_heartbeat(self):
        return super().on_heartbeat()
