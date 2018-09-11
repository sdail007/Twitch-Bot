import datetime
from datetime import timedelta


class Cooldown(object):
    @classmethod
    def fromSettings(cls, settings):
        cooldown = settings["Seconds"]
        name = settings["Alias"]
        id = settings["ID"]
        return cls(cooldown, name, id)

    def __init__(self, seconds, name=None, id=None):
        self.cooldown = seconds
        self.name = name
        self.ID = id

        self.lastUsed = datetime.datetime.now() - timedelta(seconds=self.
                                                            cooldown)

    def getKey(self):
        if self.name is not None:
            return self.name
        else:
            return self.cooldown

    def dumpAsDict(self):
        if self.ID is None:
            raise ValueError("Cannot store anonymous cooldown")
        return {"ID": self.ID, "Alias": self.name, "Seconds": self.cooldown}

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


class CooldownProvider(object):
    def __init__(self, cooldowns):
        self.Cooldowns = cooldowns
        return

    def GetCooldown(self, obj):
        if isinstance(obj, int):
            return Cooldown(obj)
        elif isinstance(obj, basestring):
            cd = next((x for x in self.Cooldowns if x.name == obj), None)
            if cd is None:
                raise IndexError
            return cd
        else:
            raise TypeError
