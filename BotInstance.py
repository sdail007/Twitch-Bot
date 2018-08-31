from TwitchConnection import TwitchConnection
from Readers import *
from Eevee import *
from RockPaperScissors import *

class BotInstance(object):
    def __init__(self, user, channel, dir):
        self.connection = TwitchConnection(user, channel)

        self.settings = Settings(dir, self.connection)

        self.components = []
        self.addons = []

        for key, value in self.settings.links.__dict__.items():
            r = self.settings.responses.Responses[value["Response"]]
            t = self.settings.triggers.Triggers[value["Trigger"]]
            r.addTrigger(t)

        self.eevee = Eevee(self.connection)
        self.rpsAdaptor = RockPaperScissorsEeveeAdaptor(self.eevee)
        self.rps = RockPaperScissorsAddon(self.eevee, self.rpsAdaptor)

        self.components.append(self.eevee)

        def MessageReceived(msg):
            print(msg)
            for key, value in self.settings.triggers.Triggers.items():
                value.invoke(msg)
            for component in self.components:
                for trigger in component.triggers:
                    trigger.invoke(msg)

        self.connection.MessageReceived.add(MessageReceived)
        self.connection.start()

    def shutdown(self):
        for component in self.components:
            component.shutdown()

    def send_message(self, msg):
        self.connection.send_message(msg)
