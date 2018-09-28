class Counter(object):
    @classmethod
    def fromSettings(cls, name, settings):
        value = settings["Value"]
        response = settings["Response"]
        return cls(name, response, value)

    def __init__(self, name, response, value=0):
        self.name = name
        self.response = response
        self.value = value

    def dumpAsDict(self):
        return {"Value": self.value, "Response": self.response}

    def Increment(self):
        self.value += 1
        return

    def Reset(self):
        self.value = 0
        return

    def getResponse(self):
        return self.response.format(self.value)
