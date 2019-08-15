from BotComponents.RockPaperScissors import *
from BotComponents.PokeBlockGame import *
from PokeBlockGameAdaptor import EeveePokeBlockGameAdaptor
from EeveeRockPaperScissorsAdaptor import RockPaperScissorsEeveeAdaptor

from Happiness import Happiness
from Hunger import Hunger
from DressUp import *
import codecs
import json


class Eevee(BotComponent):
    waitMedian = 30 * 60
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

    def __init__(self, settings_file):
        super(Eevee, self).__init__()
        self.save_file = settings_file

        self.happiness = None
        self.hunger = None
        self.dressUp = None
        self.playTimer = None
        self.PokeBlockGameAdaptor = None
        self.PokeBlockGame = None
        self.rpsAdaptor = None
        self.rpsAddon = None
        return

    def initialize(self, adaptor):
        self.adaptor = adaptor

        with codecs.open(self.save_file, encoding="utf-8-sig", mode="r") \
                as f:
            settings = json.load(f, encoding="utf-8")

        if "Happiness" in settings:
            self.happiness = Happiness(self, settings=settings[
                "Happiness"])
        else:
            self.happiness = Happiness(self)

        if "Hunger" in settings:
            self.hunger = Hunger(self, settings=settings["Hunger"])
        else:
            self.hunger = Hunger(self)

        if "DressUp" in settings:
            self.dressUp = DressUp(self,
                                   settings=settings["DressUp"])
        else:
            self.dressUp = DressUp(self)

        self.playTimer = Timer(Eevee.GetPlayInterval(), self.PlayWithMe)

        self.PokeBlockGameAdaptor = EeveePokeBlockGameAdaptor(self)
        self.PokeBlockGame = PokeBlockGameAddon(self.PokeBlockGameAdaptor)
        self.rpsAdaptor = RockPaperScissorsEeveeAdaptor(self)
        self.rpsAddon = RockPaperScissorsAddon(self.rpsAdaptor)

        self.playTimer.start()
        return

    def PlayWithMe(self):
        if self.adaptor is None:
            return

        happiness = int(self.happiness.CurrentValue)
        happiness = happiness - (happiness % 200)
        responseDict = self.happiness.Responses

        responses = responseDict[str(happiness)]
        response_count = len(responses)

        index = random.randint(0, response_count - 1)

        response = responses[index]

        self.adaptor.send_message(response)
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

