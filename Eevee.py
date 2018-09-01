
import codecs
import json
import os
import random

from EeveeResponse import EeveeResponse
from RockPaperScissors import *
from BotComponent import BotComponent

#TODO: Threshold triggers
#TODO: Rename and better identity


class Eevee(BotComponent):
    MIN_HAPPINESS = 0
    MAX_HAPPINESS = 600

    HappinessTick = 60
    PlayTick = 10 * 60

    @classmethod
    def GetPlayInterval(cls):
        delta = random.randint(-3 * 60, 3 * 60)
        wait = (7 * 60) + delta
        return wait

    def getHappinessThreshold(self):
        happiness = int(self.Settings["Happiness"])
        happiness = happiness - (happiness % 100)
        return happiness

    def __init__(self, connection, settings_dir):
        super(Eevee, self).__init__(connection)

        self.happyfile = os.path.join(settings_dir, "Eevee.json")
        with codecs.open(self.happyfile, encoding="utf-8-sig", mode="r") as f:
            self.Settings = json.load(f, encoding="utf-8")

        def HappyTick():
            self.ChangeHappiness(-1)

            self.happinessTimer = Timer(Eevee.HappinessTick, HappyTick)
            self.happinessTimer.start()
            return

        def PlayWithMe():
            happiness = self.getHappinessThreshold()
            responseDict = self.Settings["Responses"]

            responses = responseDict[str(happiness)]
            response_count = len(responses)

            index = random.randint(0, response_count - 1)

            response = responses[index]

            self.connection.send_message(response)
            self.playTimer = Timer(Eevee.GetPlayInterval(), PlayWithMe)
            self.playTimer.start()
            return

        eeveeTrigger = Trigger('!play')
        eeveeResponse = EeveeResponse(self, self.connection)
        eeveeResponse.addTrigger(eeveeTrigger)
        self.triggers.append(eeveeTrigger)

        self.happinessTimer = Timer(Eevee.HappinessTick, HappyTick)
        self.happinessTimer.start()

        self.playTimer = Timer(Eevee.GetPlayInterval(), PlayWithMe)
        self.playTimer.start()
        return

    def shutdown(self):
        self.happinessTimer.cancel()
        self.playTimer.cancel()
        return

    def MessageReceived(self, msg):
        for trigger in self.triggers:
            trigger.invoke(msg)
        return

    def ChangeHappiness(self, value):
        self.Settings["Happiness"] += value

        with codecs.open(self.happyfile, encoding="utf-8-sig", mode="w+") as f:
            json.dump(self.Settings, f, encoding="utf-8")
        return


class RockPaperScissorsEeveeAdaptor(RockPaperScissorsAdaptor):
    def __init__(self, eevee):
        super(RockPaperScissorsEeveeAdaptor, self).__init__()
        self.eevee = eevee
        return

    def started(self):
        self.eevee.connection.send_message("LETS PLAY! GO!")
        return

    def timeout(self):
        self.eevee.connection.send_message("Awww you said you'd play with me")
        self.eevee.ChangeHappiness(-5)
        return

    def response(self, msg):
        s = msg + "!!!!!!"
        self.eevee.connection.send_message(s)
        return

    def gameover(self, win):
        if win == RockPaperScissors.loss:
            self.eevee.connection.send_message("You big meanie YesYou")
            self.eevee.ChangeHappiness(-5)
        elif win == RockPaperScissors.win:
            self.eevee.connection.send_message("Yay I WIN!!!!")
            self.eevee.ChangeHappiness(30)
        else:
            self.eevee.connection.send_message("Awww... Play again?")
            self.eevee.ChangeHappiness(15)
        return

    def unexpected_command(self, msg):
        self.eevee.connection.send_message(
            "@" + msg.Sender + " we're not playing silly!")
        return
