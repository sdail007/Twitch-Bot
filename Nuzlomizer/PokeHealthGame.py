from BotInterfaces.BotComponent import BotComponent
from Commands.Trigger import Trigger, UserSpecificTrigger
from Commands.Response import CodeResponse
from EventsList.EventList import *
from Web.ThreadingSimpleServer import *
import SimpleHTTPServer

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

            if 'Balance' in settings:
                self.balance = settings['Balance']
            else:
                self.balance = 0

            self.queue = [PokeHealthGameEvent.fromSettings(recentEvent)
                          for recentEvent in settings['Queue']]
            self.rewardPoints = settings['RewardPoints']
            self.purchases = settings['Purchases']
            self.players = settings['Players']

            t = UserSpecificTrigger('!{}'.format('Purchase'), self.players)
            r = CodeResponse(10, self.spend_points)
            r.addTrigger(t)
            self.triggers.append(t)

            t1 = UserSpecificTrigger('!{}'.format('donation'), self.players)
            r1 = CodeResponse(10, self.add_donation_points)
            r1.addTrigger(t1)
            self.triggers.append(t1)

            t2 = UserSpecificTrigger('!{}'.format('follow'), self.players)
            r2 = CodeResponse(10, self.add_follow_points)
            r2.addTrigger(t2)
            self.triggers.append(t2)

            tlife = UserSpecificTrigger('!{}'.format('life'), self.players)
            rlife = CodeResponse(0, self.disposition_event)
            rlife.addTrigger(tlife)
            self.triggers.append(tlife)

            tbalance = Trigger("!{}".format("balance"))
            rbalance = CodeResponse(10, self.print_balance)
            rbalance.addTrigger(tbalance)
            self.triggers.append(tbalance)

        self.connection.EventReceived.add(self.eventReceived)

        self.ConnectionHandler = None
        self.start_server('127.0.0.1', 1112)

        webServer = ThreadingSimpleServer(('127.0.0.1', 8000),
                                          SimpleHTTPServer.SimpleHTTPRequestHandler)

        webServerThread = threading.Thread(target=webServer.serve_forever)
        webServerThread.daemon = True
        webServerThread.start()
        return

    def start_server(self, ip, port):
        self.ConnectionHandler = WebsocketServer(port, host=ip)
        self.ConnectionHandler.set_fn_new_client(self.NewClient)

        serverThread = threading.Thread(
            target=self.ConnectionHandler.run_forever)
        serverThread.daemon = True
        serverThread.start()
        return

    def NewClient(self, client, server):
            self.ConnectionHandler.send_message(client,
                                                json.dumps({"balance": self.balance}))
            return

    def dumpAsDict(self):
        q = []
        for recentEvent in self.queue:
            q.append(recentEvent.dumpAsDict())
        return {"Balance": self.balance,
                "RewardPoints": self.rewardPoints,
                "Purchases": self.purchases,
                "Players": self.players,
                "Queue": q}

    def Save(self):
        with codecs.open(self.settingsFile, encoding="utf-8-sig", mode="w+") as f:
            json.dump(self.dumpAsDict(), f, encoding="utf-8", indent=4,
                      sort_keys=True)
        self.events.Save()
        return

    def print_balance(self, sender, message, *args):
        self.connection.send_message('Points remaining: {}'.format(self.balance))
        return

    def add_follow_points(self, sender, message, *args):
        earnedPoints = self.rewardPoints['FollowPoints']
        self.SubmitEvent('New Follow!', earnedPoints)
        return

    def add_donation_points(self, sender, message, *args):
        param = message.Message.split()[1]
        points = float(param)
        points = round(points, 2)

        print points

        multiplier = self.rewardPoints['DonationPoints']
        earnedPoints = points * multiplier
        self.SubmitEvent('New Donation!', earnedPoints)
        return

    def disposition_event(self, sender, message, *args):
        params = message.Message.split()[1:]
        if len(params) > 0:
            event = None
            if params[0] == "+":
                event = self.queue.pop(0)
            elif params[0] == "-":
                event = self.queue.pop(0)
                event.valueChange = -event.valueChange

            if event is not None:
                self.balance += event.valueChange
                self.events.add_event(event)
                self.events.Save()
                self.Save()
                remaining = len(self.queue)
                if remaining > 0:
                    sender.send_message('{} items remaining in the queue'
                                        .format(remaining))
        else:
            event = self.queue[0]
            if event is not None:
                sender.send_message("Next Event: {}".format(event))
            else:
                sender.send_message("Next Event: {}".format(event))
        return

    def spend_points(self, sender, message, *args):
        item = message.Message.split()[1]
        item = item.lower()
        if item in self.purchases:
            cost = self.purchases[item]
            if self.balance - cost >= 0:
                sender.send_message("{} purchased! Points remaining: {}".format(item, self.balance))
                self.SubmitEvent('{} purchased!'.format(item), -cost)
            else:
                sender.send_message("You can't afford a {}!".format(item))
        else:
            sender.send_message("Unknown item {}!".format(item))

        return

    def eventReceived(self, sender, message):
        if 'command' in message:
            # Sub
            if message['command'] == 'USERNOTICE':
                if 'subplan' in message:
                    # gift sub
                    if message['msgid'] == 'subgift' and message['user'] in \
                            self.players:
                        #gift from who dis
                        rewardRatio = self.rewardPoints['GiftSubPoints']
                        self.SubmitEvent('New Gift sub', rewardRatio)
                    else:
                        if message['subplan'] == 'Prime':
                            planPoints = 1000
                            planText = message['subplan']
                        else:
                            planPoints = int(message['subplan'])
                            planText = "TIER " + message['subplan'][0]

                        rewardRatio = self.rewardPoints['SubPoints']
                        moneyAwarded = planPoints * rewardRatio
                        self.QueueEvent('NEW {} SUB'.format(planText), moneyAwarded)
                if 'raidDisplayName' in message:
                    raider = message['raidDisplayName']
                    raidpoints = self.rewardPoints['RaidPoints']
                    self.SubmitEvent('{} Raid!'.format(raider), raidpoints)
            # host
            elif message['command'] == 'HOSTTARGET':
                channel = message['channel']
                raidpoints = self.rewardPoints['RaidPoints']
                self.SubmitEvent('{} Host!'.format(channel), raidpoints)
            # Bits
            elif message['command'] == 'PRIVMSG' \
                    and 'bits' in message\
                    and message['bits'] is not None:
                bitCount = int(message['bits'])
                rewardRatio = self.rewardPoints['BitPoints']
                moneyAwarded = bitCount * rewardRatio
                self.QueueEvent('Bits get!', moneyAwarded)
        return

    def QueueEvent(self, text, value):
        newEvent = PokeHealthGameEvent(datetime.now(), text, value)
        self.queue.append(newEvent)
        self.connection.send_message('Event Added!')
        return

    def SubmitEvent(self, text, value):
        newEvent = PokeHealthGameEvent(datetime.now(), text, value)
        self.update_balance(newEvent.valueChange)
        self.events.add_event(newEvent)
        self.Save()
        self.ConnectionHandler.send_message_to_all(json.dumps({"balance": self.balance}))
        return

    def update_balance(self, valueChange):
        self.balance += valueChange
        if self.balance <= 0:
            self.connection.send_message('G A M E O V E R')
            self.balance = 0
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

