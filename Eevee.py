from RockPaperScissors import *
from PokeBlockGame import *
from BotComponent import BotComponent
from Happiness import Happiness
from Hunger import Hunger
from DressUp import *

class Eevee(BotComponent):
    def __init__(self, connection, settings):
        super(Eevee, self).__init__(connection)
        self.settings = settings

        self.happiness = Happiness(connection, self.settings)
        self.hunger = Hunger(connection, self.settings)
        self.dressUp = DressUp(connection, self.settings, self.happiness)

        def printPlayCommands(sender, msg, *args):
            cmds = [t.text for t in self.happiness.triggers]
            cmdstring = ", ".join(cmds)
            output = "I can play games! " + cmdstring
            self.connection.send_message(output)
            return

        eeveeTrigger = Trigger('!play')
        eeveeResponse = CodeResponse(5, printPlayCommands)
        eeveeResponse.addTrigger(eeveeTrigger)
        self.triggers.append(eeveeTrigger)

        self.triggers.extend(self.hunger.triggers)
        self.triggers.extend(self.dressUp.triggers)
        return

    def shutdown(self):
        self.happiness.happinessTimer.cancel()
        self.happiness.playTimer.cancel()
        self.hunger.hungerTimer.cancel()
        return


class RockPaperScissorsEeveeAdaptor(RockPaperScissorsAdaptor):
    def __init__(self, eevee):
        super(RockPaperScissorsEeveeAdaptor, self).__init__()
        self.eevee = eevee
        return

    def register(self, addon):
        self.eevee.happiness.triggers.extend(addon.triggers)
        return

    def started(self):
        self.eevee.connection.send_message("LETS PLAY! GO!")
        return

    def timeout(self):
        self.eevee.connection.send_message("Awww you said you'd play with me")
        self.eevee.happiness.Update(-5)
        return

    def response(self, msg):
        s = msg + "!!!!!!"
        self.eevee.connection.send_message(s)
        return

    def gameover(self, win):
        if win == RockPaperScissors.loss:
            self.eevee.connection.send_message("You big meanie YesYou")
            self.eevee.happiness.Update(-5)
        elif win == RockPaperScissors.win:
            self.eevee.connection.send_message("Yay I WIN!!!!")
            self.eevee.happiness.Update(80)
        else:
            self.eevee.connection.send_message("Awww... Play again?")
            self.eevee.happiness.Update(50)
        return

    def unexpected_command(self, msg):
        self.eevee.connection.send_message(
            "@" + msg.Sender + " we're not playing silly!")
        self.eevee.happiness.Update(10)
        return


class EeveePokeBlockGameAdaptor(PokeBlockGameAdaptor):

    responses = [
        "AWW That's no fun!",
        "I'm still hungry",
        "mmmMMMmmmm",
        "Tasty!",
        "THICCCCC"
    ]

    def __init__(self, eevee):
        super(EeveePokeBlockGameAdaptor, self).__init__()
        self.eevee = eevee
        return

    def register(self, addon):
        self.eevee.happiness.triggers.extend(addon.triggers)
        self.eevee.hunger.triggers.extend(addon.triggers)
        return

    def started(self):
        self.eevee.connection.send_message("I LOVE POKEBLOCKS")
        return

    def gameover(self, result):
        count = min(len(EeveePokeBlockGameAdaptor.responses) - 1, len(result))
        reward = count * 25
        self.eevee.happiness.Update(reward)
        self.eevee.hunger.Update(reward)

        response = EeveePokeBlockGameAdaptor.responses[count]
        self.eevee.connection.send_message(response)
        return

    def unexpected_command(self, msg):
        return
