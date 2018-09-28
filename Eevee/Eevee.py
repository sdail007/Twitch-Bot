from BotComponents.RockPaperScissors import *
from BotComponents.PokeBlockGame import *
from Happiness import Happiness
from Hunger import Hunger
from DressUp import *
import codecs
import json


class Eevee(BotComponent):
    waitMedian = 10 * 60
    waitDelta = 2 * 60

    @classmethod
    def GetPlayInterval(cls):
        delta = random.randint(- Eevee.waitDelta, Eevee.waitDelta)
        return Eevee.waitMedian + delta

    def dump_as_dict(self):
        '''
        Dump current class as dict for storage
        :return:
        '''
        return {"Happiness": self.happiness.dump_as_dict(),
                "Hunger": self.hunger.dump_as_dict(),
                "DressUp": self.dressUp.dump_as_dict()}

    def __init__(self, connection, settings_file):
        super(Eevee, self).__init__(connection)
        self.save_file = settings_file

        with codecs.open(self.save_file, encoding="utf-8-sig", mode="r") \
                as f:
            settings = json.load(f, encoding="utf-8")

        if "Happiness" in settings:
            self.happiness = Happiness(connection,
                                       settings=settings["Happiness"])
        else:
            self.happiness = Happiness(connection)

        if "Hunger" in settings:
            self.hunger = Hunger(connection,
                                 settings=settings["Hunger"])
        else:
            self.hunger = Hunger(connection)

        if "DressUp" in settings:
            self.dressUp = DressUp(connection, self.happiness,
                                   settings=settings["DressUp"])
        else:
            self.dressUp = DressUp(connection)

        self.playTimer = Timer(Eevee.GetPlayInterval(), self.PlayWithMe)

        self.triggers.extend(self.happiness.triggers)
        self.triggers.extend(self.hunger.triggers)
        self.triggers.extend(self.dressUp.triggers)
        self.playTimer.start()
        return

    def PlayWithMe(self):
        happiness = int(self.happiness.CurrentValue)
        happiness = happiness - (happiness % 200)
        responseDict = self.happiness.Responses

        responses = responseDict[str(happiness)]
        response_count = len(responses)

        index = random.randint(0, response_count - 1)

        response = responses[index]

        self.connection.send_message(response)
        self.playTimer = Timer(Eevee.GetPlayInterval(), self.PlayWithMe)
        self.playTimer.start()
        return

    def shutdown(self):
        self.playTimer.cancel()
        self.happiness.healthTimer.cancel()
        self.hunger.healthTimer.cancel()
        self.dressUp.shutdown()

        with codecs.open(self.save_file, encoding="utf-8-sig", mode="w+") as f:
            json.dump(self.dump_as_dict(), f, encoding="utf-8", indent=4,
                      sort_keys=True)
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
