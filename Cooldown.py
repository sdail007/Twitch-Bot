import datetime
from datetime import timedelta


class Cooldown(object):
    def __init__(self, sec):
        self.cooldown = sec
        self.lastUsed = datetime.datetime.now() - timedelta(seconds=self.
                                                            cooldown)

    def Consume(self):
        threshold = datetime.datetime.now() - timedelta(seconds=self.cooldown)
        if threshold < self.lastUsed:
            return False
        self.lastUsed = datetime.datetime.now()
        return True

    def __str__(self):
        return str(self.cooldown)
