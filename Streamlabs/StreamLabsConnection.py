import websocket
import codecs
import json
import threading
from socketIO_client import SocketIO, LoggingNamespace


class StreamLabsConnection(object):
    def __init__(self, file):
        with codecs.open(file, encoding='utf-8-sig', mode='r') as f:
            settings = json.load(f, encoding='utf-8')

        token = settings["Token"]
        apiKey = settings["ApiKey"]

        target = "https://sockets.streamlabs.com:443?token=${}".format(token)

        streamlabs = SocketIO(target, wait_for_connection=True, transports=['websocket'])
        streamlabs.on('connect', self.connected)
        streamlabs.on('event', self.event)
        streamlabs.wait()

        return

    def event(self, event):
        return

    def connected(self):
        print "connected to streamlabs"
        return

    def error(self, error):
        print "error: ", error
        return

    def closed(self, reason):
        print "reason: ", reason
        return

