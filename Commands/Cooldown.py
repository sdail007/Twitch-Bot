import datetime
from datetime import timedelta


class Cooldown(object):
    def __init__(self, seconds, name=None):
        self.cooldown = seconds
        self.name = name

        self.lastUsed = datetime.datetime.now() - timedelta(seconds=self.
                                                            cooldown)

    def getKey(self):
        if self.name is not None:
            return self.name
        else:
            return self.cooldown

    def Consume(self):
        threshold = datetime.datetime.now() - timedelta(seconds=self.cooldown)
        if threshold < self.lastUsed:
            return False
        self.lastUsed = datetime.datetime.now()
        return True

    def __str__(self):
        return str(self.cooldown)

    def __repr__(self):
        return str(self)

