from BotInterfaces.BotComponent import BotComponent
from Commands.Trigger import ContainsTrigger
from Commands.Response import CodeResponse
from Web.websocket_server import WebsocketServer
from Web.ThreadingSimpleServer import *
import SimpleHTTPServer

import threading
import codecs
import json


class KappuAnimationAdaptor(BotComponent):
    def __init__(self, connection, file):
        super(KappuAnimationAdaptor, self).__init__(connection)
        self.file = file
        if self.file is not None:
            with codecs.open(self.file, encoding="utf-8-sig", mode="r") as f:
                settings = json.load(f, encoding="utf-8")

            self.connectioninfo = settings["ConnectionInfo"]
            port = self.connectioninfo['Port']
            ip = self.connectioninfo['IP']
        else:
            port = 1000,
            ip = '127.0.0.1'

        self.ConnectionHandler = WebsocketServer(port, host=ip)

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

        webServer = ThreadingSimpleServer(('', 8000),
                                          SimpleHTTPServer.SimpleHTTPRequestHandler)

        webServerThread = threading.Thread(target=webServer.serve_forever)
        webServerThread.daemon = True

        server.start()
        webServerThread.start()
        return

    def SendMessage(self, sender, message, *args):
        kappu = args[0][0]
        self.ConnectionHandler.send_message_to_all(kappu)
        return

    def dumpAsDict(self):
        return {"ConnectionInfo": self.connectioninfo}

    def Save(self):
        with codecs.open(self.file, encoding="utf-8-sig", mode="w+") as f:
            json.dump(self.dumpAsDict(), f, encoding="utf-8", indent=2,
                      sort_keys=True)
        return

    def shutdown(self):
        self.ConnectionHandler.shutdown()
        self.Save()
        return
