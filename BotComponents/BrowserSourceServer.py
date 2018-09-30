from Commands.BotComponent import BotComponent
from Commands.Trigger import ContainsTrigger
from Commands.Response import CodeResponse
import logging
from websocket_server import *
import thread


class BrowserSourceServer(BotComponent):
    def __init__(self, connection):
        super(BrowserSourceServer, self).__init__(connection)
        self.server = WebsocketServer(12345, host='127.0.0.1')

        t = ContainsTrigger('KappuNadeshiko')
        r = CodeResponse(10, self.sendMessage, 'KappuNadeshiko')
        r.addTrigger(t)

        t2 = ContainsTrigger('KappuRin')
        r2 = CodeResponse(10, self.sendMessage, 'KappuRin')
        r2.addTrigger(t2)

        self.triggers.append(t)
        self.triggers.append(t2)
        return

    def shutdown(self):
        self.server.shutdown()
        return

    def start(self):
        def run(*args):
            self.server.run_forever()
        thread.start_new_thread(run, ())
        return

    def sendMessage(self, sender, message, *args):
        msg = args[0][0]
        print msg
        self.server.send_message_to_all(msg)
        return

    def client_connected(self, client, server):
        print 'New client connected'
        return
