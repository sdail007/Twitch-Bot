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

        self.components = []

        for key, value in self.links.__dict__.items():
            r = self.responses.Responses[value["Response"]]
            t = self.triggers.Triggers[value["Trigger"]]
            r.addTrigger(t)
            #print "linking: ", t, " to ", r

        self.components.append(Eevee(self.connection))

        def MessageReceived(msg):
            print(msg)
            for key, value in self.triggers.Triggers.items():
                value.invoke(msg)
            for component in self.components:
                for trigger in component.triggers:
                    trigger.invoke(msg)

        self.connection.MessageReceived.add(MessageReceived)

        thread.start_new_thread(self.connection.start(), ())

    def shutdown(self):
        for component in self.components:
            component.shutdown()

    def send_message(self, msg):
        self.connection.send_message(msg)
