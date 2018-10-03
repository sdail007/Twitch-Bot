from Commands.BotComponent import BotComponent
from Commands.Trigger import Trigger
from Commands.Response import CodeResponse
from Web.websocket_server import WebsocketServer
from Twitch.TwitchConnection import *

from datetime import datetime
import codecs
import json
import threading


class PokeHealthGame(BotComponent):
    def __init__(self, twitchConnection, file=None):
        super(PokeHealthGame, self).__init__(twitchConnection)

        if file is not None:
            self.file = file

            with codecs.open(self.file, encoding="utf-8-sig", mode="r") as f:
                settings = json.load(f, encoding="utf-8")

            self.value = settings['Value']
            self.recentEvents = [PokeHealthGameEvent.fromSettings(recentEvent)
                                 for recentEvent in settings['RecentEvents']]
        else:
            self.value = 0
            self.recentEvents = []
            #make a file

        self.ConnectionHandler = WebsocketServer(1000, host='127.0.0.1')

        self.connection.EventReceived.add(self.eventReceived)

        t = Trigger('!polarbear')
        r = CodeResponse(10, self.NewSub)
        r.addTrigger(t)

        t2 = Trigger('!owl')
        r2 = CodeResponse(10, self.NewBits)
        r2.addTrigger(t2)

        t3 = Trigger('!fox')
        r3 = CodeResponse(10, self.NewFollow)
        r3.addTrigger(t3)

        self.triggers.append(t)
        self.triggers.append(t2)
        self.triggers.append(t3)

        self.ConnectionHandler.set_fn_new_client(self.NewClient)

        server = threading.Thread(target=self.ConnectionHandler.run_forever)
        server.daemon = True
        server.start()
        return

    def NewClient(self, client, server):
        lastThree = self.recentEvents[:3]
        for recentEvent in lastThree:
            self.ConnectionHandler.send_message(client, recentEvent.text)
        return

    def dumpAsDict(self):
        recentEvents = []
        for recentEvent in self.recentEvents:
            recentEvents.append(recentEvent.dumpAsDict())
        return {"Value": self.value, "RecentEvents": recentEvents}

    def Save(self):
        with codecs.open(self.file, encoding="utf-8-sig", mode="w+") as f:
            json.dump(self.dumpAsDict(), f, encoding="utf-8", indent=4,
                      sort_keys=True)
        return

    def eventReceived(self, sender, message):
        if 'command' in message:
            if message['command'] == 'USERNOTICE' and 'subplan' in message:
                self.SubmitEvent('NEW SUB', 100)

        return

    def NewSub(self, sender, message, *args):
        self.SubmitEvent('Polar Bears are the Coolest Thing Ever', 100)
        return

    def NewBits(self, sender, message, *args):
        self.SubmitEvent('Mr. Owl think you are pretty coo', 50)
        return

    def NewFollow(self, sender, message, *args):
        self.SubmitEvent('The fox says you are a beautiful person', 10)
        return

    def SubmitEvent(self, text, value):
        newEvent = PokeHealthGameEvent(datetime.now(), text,
                                       value)
        self.value += value
        self.recentEvents.append(newEvent)
        self.ConnectionHandler.send_message_to_all(newEvent.text)
        self.Save()
        return

    def shutdown(self):
        self.ConnectionHandler.shutdown()
        self.Save()
        return


class PokeHealthGameEvent(object):
    @classmethod
    def fromSettings(cls, settings):
        time = datetime.strptime(settings['Time'], '%Y-%m-%d %H:%M:%S.%f')
        text = settings['EventText']
        valueChange = settings['ValueChange']
        return cls(time, text, valueChange)

    def __init__(self, time, text, valueChange):
        self.time = time
        self.text = text
        self.valueChange =valueChange
        return

    def dumpAsDict(self):
        return {"Time": str(self.time), "EventText": self.text, "ValueChange":
            self.valueChange}

