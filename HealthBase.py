import random
from threading import Timer

from BotComponent import BotComponent


class HealthBase(BotComponent):
    MIN_VALUE = 0
    MAX_VALUE = 600

    Tick = 36

    def dump_as_dict(self):
        '''
        :return:
        '''
        return {"CurrentValue": self.CurrentValue,
                "Responses": self.Responses}

    def __init__(self, connection, settings):
        super(HealthBase, self).__init__(connection)

        if settings:
            self.CurrentValue = settings["CurrentValue"]
            self.Responses = settings["Responses"]
        else:
            self.CurrentValue = None
            self.Responses = {}

        self.Updated = None

        self.healthTimer = Timer(HealthBase.Tick, self.HealthTick)
        self.healthTimer.start()
        return

    def HealthTick(self):
        self.Update(-1)
        self.healthTimer = Timer(HealthBase.Tick, self.HealthTick)
        self.healthTimer.start()
        return

    def __del__(self):
        self.healthTimer.cancel()
        return

    def print_commands(self):
        return

    def Update(self, value):
        self.CurrentValue = HealthBase.Clamp(self.CurrentValue + value)

    def GetResponse(self):
        temp = self.CurrentValue - (self.CurrentValue % 200)
        responses = self.Responses[str(temp)]
        response_count = len(responses)
        index = random.randint(0, response_count - 1)

        return self.Responses[index]

    @classmethod
    def Clamp(cls, value):
        return min(max(HealthBase.MIN_VALUE, value), HealthBase.MAX_VALUE)
