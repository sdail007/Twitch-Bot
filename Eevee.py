from EeveeResponse import EeveeResponse
from RockPaperScissors import *


class Eevee(object):
    MIN_HAPPINESS = 0
    MAX_HAPPINESS = 600

    HappinessTick = 60

    def __init__(self, connection):
        self.connection = connection

        self.Happiness = 300
        self.triggers = []
        self.t = None

        def HappyTick():
            self.ChangeHappiness(-1)
            self.t = Timer(Eevee.HappinessTick, HappyTick)
            self.t.start()
            return

        RockPaperScissorsGame.Initialize(self)

        eeveeTrigger = Trigger('!play')
        eeveeResponse = EeveeResponse(self, self.connection)
        eeveeResponse.addTrigger(eeveeTrigger)
        self.triggers.append(eeveeTrigger)

        HappyTick()
        return

    def __del__(self):
        self.STAHP()
        return

    def STAHP(self):
        self.t.cancel()
        return

    def MessageReceived(self, msg):
        for trigger in self.triggers:
            trigger.invoke(msg)
        return

    def ChangeHappiness(self, value):
        self.Happiness += value
        return
