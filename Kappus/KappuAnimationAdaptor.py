from Commands.BotComponent import BotComponent
from Commands.Trigger import ContainsTrigger
from Commands.Response import CodeResponse
from Web.websocket_server import WebsocketServer
from Web.ThreadingSimpleServer import *
import SimpleHTTPServer

import threading


class KappuAnimationAdaptor(BotComponent):
    def __init__(self, connection, file):
        super(KappuAnimationAdaptor, self).__init__(connection)

        self.ConnectionHandler = WebsocketServer(12345, host='127.0.0.1')
        webServer = ThreadingSimpleServer(('', 8000),
                                          SimpleHTTPServer.SimpleHTTPRequestHandler)

        t = ContainsTrigger('KappuNadeshiko')
        r = CodeResponse(10, self.SendMessage, 'KappuNadeshiko')
        r.addTrigger(t)

        t2 = ContainsTrigger('KappuRin')
        r2 = CodeResponse(10, self.SendMessage, 'KappuRin')
        r2.addTrigger(t2)

        self.triggers.append(t)
        self.triggers.append(t2)

        server = threading.Thread(target=self.ConnectionHandler.run_forever)
        server.daemon = True

        webServerThread = threading.Thread(target=webServer.serve_forever)
        webServerThread.daemon = True

        server.start()
        webServerThread.start()
        return

    def SendMessage(self, sender, message, *args):
        kappu = args[0][0]
        self.ConnectionHandler.send_message_to_all(kappu)
        return

    def shutdown(self):
        self.ConnectionHandler.shutdown()
        return
