from TwitchConnection import TwitchConnection
from Readers import *
from Eevee import *
from EeveeSettings import EeveeSettings
from PokeBlockGame import PokeBlockGameAddon


class BotInstance(object):
    def __init__(self, user, channel, settings_dir):
        self.connection = TwitchConnection(user, channel)

        self.settings = Settings(settings_dir)

        self.components = []
        self.addons = []

        for key, value in self.settings.links.__dict__.items():
            r = self.settings.responses.Responses[value["Response"]]
            t = self.settings.triggers.Triggers[value["Trigger"]]
            r.addTrigger(t)

        eevee_settings = EeveeSettings(os.path.join(settings_dir, "Eevee.json"))

        self.eevee = Eevee(self.connection, eevee_settings)
        self.rpsAdaptor = RockPaperScissorsEeveeAdaptor(self.eevee)
        self.rps = RockPaperScissorsAddon(self.eevee, self.rpsAdaptor)

        self.bbAdaptor = EeveePokeBlockGameAdaptor(self.eevee)
        self.berryBlender = PokeBlockGameAddon(self.eevee, self.bbAdaptor)

        self.components.append(self.eevee)

        def MessageReceived(sender, msg):
            print(msg)
            for key, value in self.settings.triggers.Triggers.items():
                value.invoke(sender, msg)
            for component in self.components:
                for trigger in component.triggers:
                    trigger.invoke(sender, msg)

        self.connection.MessageReceived.add(MessageReceived)
        self.connection.start()

    def shutdown(self):
        for component in self.components:
            component.shutdown()

    def send_message(self, msg):
        self.connection.send_message(msg)
