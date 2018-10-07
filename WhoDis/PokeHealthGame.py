from Commands.BotComponent import BotComponent
from Commands.Trigger import Trigger
from Commands.Response import CodeResponse
from Commands.Cooldown import Cooldown
from EventsList.EventList import *

from datetime import datetime
import codecs
import json
import os


class PokeHealthGame(BotComponent):
    def __init__(self, twitchConnection, folder):
        super(PokeHealthGame, self).__init__(twitchConnection)

        eventsListFile = os.path.join(folder, "Events.json")
        self.settingsFile = os.path.join(folder, "PokeHealthGame.json")

        self.events = EventList(PokeHealthGameEvent, eventsListFile)

        with codecs.open(self.settingsFile, encoding="utf-8-sig", mode="r") as f:
            settings = json.load(f, encoding="utf-8")

            if 'Value' in settings:
                self.value = settings['Value']
            else:
                self.value = 0

            self.subpoints = settings['SubPoints']
            self.bitpoints = settings['BitPoints']
            self.purchases = settings['Purchases']

            t = Trigger('!{}'.format('Purchase'))
            r = CodeResponse(10, self.spend_points)
            r.addTrigger(t)
            self.triggers.append(t)

        self.connection.EventReceived.add(self.eventReceived)
        return

    def dumpAsDict(self):
        return {"Value": self.value,
                "SubPoints": self.subpoints,
                "BitPoints": self.bitpoints,
                "Purchases": self.purchases}

    def Save(self):
        with codecs.open(self.settingsFile, encoding="utf-8-sig", mode="w+") as f:
            json.dump(self.dumpAsDict(), f, encoding="utf-8", indent=4,
                      sort_keys=True)
        self.events.Save()
        return

    def spend_points(self, sender, message, *args):
        item = message.Message.split()[1]
        if item in self.purchases:
            cost = self.purchases[item]
            if self.value - cost >= 0:
                self.value -= cost
                sender.send_message("{} purchased! Points remaining: {}".format(item, self.value))
            else:
                sender.send_message("You can't afford a {}!".format(item))

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
        newEvent = PokeHealthGameEvent(datetime.now(), text, value)
        self.value += value
        self.events.add_event(newEvent)
        self.Save()
        return

    def shutdown(self):
        self.events.Save()
        self.Save()
        return


class PokeHealthGameEvent(Event):
    @classmethod
    def fromSettings(cls, settings):
        time = datetime.strptime(settings['Time'], '%Y-%m-%d %H:%M:%S.%f')
        text = settings['EventText']
        valueChange = settings['ValueChange']
        return cls(time, text, valueChange)

    def __init__(self, time, text, valueChange):
        super(PokeHealthGameEvent, self).__init__(text)
        self.time = time
        self.valueChange = valueChange
        return

    def dumpAsDict(self):
        return {"Time": str(self.time), "EventText": self.text, "ValueChange":
            self.valueChange}

    def __str__(self):
        return self.text

