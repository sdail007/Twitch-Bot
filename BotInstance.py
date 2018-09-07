from TwitchConnection import TwitchConnection
from Readers import *
from Eevee import *
from EeveeSettings import EeveeSettings
from PokeBlockGame import PokeBlockGameAddon
from DressUp import *


class BotInstance(object):
    def __init__(self, user, channel, settings_dir):
        self.connection = TwitchConnection(user, channel)

        self.components = []
        self.addons = []

        self.extraCommands = CustomCommandGroup(settings_dir, self.connection)
        self.components.append(self.extraCommands)

        eevee_settings = EeveeSettings(os.path.join(settings_dir, "Eevee.json"))

        self.eevee = Eevee(self.connection, eevee_settings)
        self.rpsAdaptor = RockPaperScissorsEeveeAdaptor(self.eevee)
        self.rps = RockPaperScissorsAddon(self.eevee, self.rpsAdaptor)

        self.bbAdaptor = EeveePokeBlockGameAdaptor(self.eevee)
        self.berryBlender = PokeBlockGameAddon(self.eevee, self.bbAdaptor)

        self.components.append(self.eevee)

        def MessageReceived(sender, msg):
            print(msg)
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
