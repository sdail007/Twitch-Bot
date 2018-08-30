import thread
from TwitchConnection import TwitchConnection
import Readers
from Eevee import Eevee


class BotInstance(object):
    def __init__(self, user, channel, dir):
        self.connection = TwitchConnection(user, channel)

        self.triggers = Readers.Triggers(dir)
        self.cooldowns = Readers.Cooldowns(dir)
        self.responses = Readers.Responses(dir, self.connection, self.cooldowns)
        self.links = Readers.Links(dir)

        for key, value in self.links.__dict__.items():
            r = self.responses.Responses[value["Response"]]
            t = self.triggers.Triggers[value["Trigger"]]
            r.addTrigger(t)
            #print "linking: ", t, " to ", r

        self.eevee = Eevee(self.connection)

        def MessageReceived(msg):
            print(msg)
            for key, value in self.triggers.Triggers.items():
                value.invoke(msg)
            self.eevee.MessageReceived(msg)

        self.connection.MessageReceived.add(MessageReceived)

        def startBot():
            self.connection.start()

        thread.start_new_thread(startBot, ())

    def send_message(self, msg):
        self.connection.send_message(msg)
