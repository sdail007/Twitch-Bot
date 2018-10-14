import os
import codecs
import json
import importlib


class BotInstance(object):
    def __init__(self, connection, settings_dir):
        self.connection = connection

        self.components = []
        self.addons = []

        setupfile = os.path.join(settings_dir, "setup.json")
        with codecs.open(setupfile, encoding="utf-8-sig", mode="r") as f:
            setup = json.load(f, encoding="utf-8")

            for componentSetting in setup['components']:
                #Get ClassType
                module_name = str(componentSetting['type'])
                module = importlib.import_module(module_name)
                classname = str(module_name.split('.')[-1])
                myClass = getattr(module, classname)

                #Get settings file
                file = str(componentSetting['file'])
                path = os.path.join(settings_dir, file)

                component = myClass(self.connection, path)

                self.components.append(component)

        '''
        self.kappus = KappuAnimationAdaptor(self.connection)
        self.components.append(self.kappus)

        pokeHealthFile = os.path.join(settings_dir, "PokeHealthGame")
        self.pokeHealth = PokeHealthGame(self.connection, pokeHealthFile)
        self.components.append(self.pokeHealth)

        commandsGroupFolder = os.path.join(settings_dir, "CommandsGroup")
        self.extraCommands = CustomCommandGroup(self.connection, commandsGroupFolder)
        self.components.append(self.extraCommands)

        countersFile = os.path.join(settings_dir, "Counters.json")
        self.Counters = CountersGroup(self.connection, countersFile)
        self.components.append(self.Counters)

        countersFile = os.path.join(settings_dir, "OtherCounters.json")
        self.OtherCounters = CountersGroup(self.connection, countersFile)
        self.components.append(self.OtherCounters)

        settings = os.path.join(settings_dir, "Eevee.json")
        self.eevee = Eevee(self.connection, settings)

        self.rpsAdaptor = RockPaperScissorsEeveeAdaptor(self.eevee)
        self.rps = RockPaperScissorsAddon(self.eevee, self.rpsAdaptor)

        self.bbAdaptor = EeveePokeBlockGameAdaptor(self.eevee)
        self.berryBlender = PokeBlockGameAddon(self.eevee, self.bbAdaptor)

        self.components.append(self.eevee)
        '''

        def MessageReceived(sender, msg):
            print(msg)
            for component in self.components:
                for trigger in component.triggers:
                    trigger.invoke(sender, msg)

        self.connection.MessageReceived.add(MessageReceived)

    def start(self):
        self.connection.start()
        return

    def shutdown(self):
        self.connection.stop()
        for component in self.components:
            component.shutdown()

    def send_message(self, msg):
        self.connection.send_message(msg)

    def __del__(self):
        self.shutdown()
