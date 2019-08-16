from BotInterfaces.BotComponent import BotComponent
from Commands.Trigger import ContainsTrigger
from Commands.Response import CodeResponse
from Web.websocket_server import WebsocketServer
from Web.ThreadingSimpleServer import *

import threading
import codecs
import json


class KappuAnimationAdaptor(BotComponent):
    def __init__(self, file):
        super(KappuAnimationAdaptor, self).__init__()
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
        return

    def initialize(self, adaptor):
        t = adaptor.trigger_factory\
            .create_regex_trigger(r".*KappuNadeshiko.*")
        t2 = adaptor.trigger_factory\
            .create_regex_trigger(r".*KappuRin.*")

        r = CodeResponse(10, self.SendMessage, 'KappuNadeshiko')
        r2 = CodeResponse(10, self.SendMessage, 'KappuRin')

        r.addTrigger(t)
        r2.addTrigger(t2)

        server = threading.Thread(target=self.ConnectionHandler.run_forever)
        server.daemon = True

        ThreadingSimpleServer.Start()
        server.start()
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
