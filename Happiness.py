from threading import Timer
from BotComponent import BotComponent
import random


class Happiness(BotComponent):
    MIN_HAPPINESS = 0
    MAX_HAPPINESS = 600

    HappinessTick = 36
    PlayTick = 10 * 60

    @classmethod
    def GetPlayInterval(cls):
        delta = random.randint(-2 * 60, 2 * 60)
        wait = (10 * 60) + delta
        return wait

    def __init__(self, connection, eevee_settings):
        super(Happiness, self).__init__(connection)
        self.settings = eevee_settings

        def HappyTick():
            self.Update(-1)
            self.happinessTimer = Timer(Happiness.HappinessTick, HappyTick)
            self.happinessTimer.start()
            return

        def PlayWithMe():
            happiness = self.getHappinessThreshold()
            responseDict = self.settings.Responses

            responses = responseDict[str(happiness)]
            response_count = len(responses)

            index = random.randint(0, response_count - 1)

            response = responses[index]

            self.connection.send_message(response)
            self.playTimer = Timer(Happiness.GetPlayInterval(), PlayWithMe)
            self.playTimer.start()
            return

        self.playTimer = Timer(Happiness.GetPlayInterval(), PlayWithMe)
        self.playTimer.start()

        self.happinessTimer = Timer(Happiness.HappinessTick, HappyTick)
        self.happinessTimer.start()

    def Clamp(self, value):
        return min(max(Happiness.MIN_HAPPINESS, value), Happiness.MAX_HAPPINESS)

    def getHappinessThreshold(self):
        happiness = int(self.settings.Happiness)
        happiness = happiness - (happiness % 100)
        return happiness

    def Update(self, value):
        newHappiness = self.settings.Happiness + value
        self.settings.Happiness = self.Clamp(newHappiness)
        self.settings.save()
