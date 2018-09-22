from Cooldown import *
from time import sleep


class ResponseBase(object):
    def __init__(self, cooldown=10):
        if isinstance(cooldown, int):
            self.cooldown = Cooldown(cooldown)
        elif isinstance(cooldown, Cooldown):
            self.cooldown = cooldown
        else:
            raise TypeError('cooldown must be int or Cooldown')

    def addTrigger(self, trigger):
        trigger.Triggered.add(self.respond)

    def respond(self, sender, message):
        return


class Response(ResponseBase):
    @classmethod
    def fromSettings(cls, settings, cooldownProvider=CooldownProvider([])):
        ID = settings["ID"]
        string = settings["text"]
        cooldown = cooldownProvider.GetCooldown(settings["cooldown"])
        return cls(string, cooldown, ID)

    def __init__(self, string, cooldown=10, ID=0):
        super(Response, self).__init__(cooldown)
        self.ID = ID
        self.string = string
        return

    def dumpAsDict(self):
        return {"ID": self.ID, "text": self.string,
                "cooldown": self.cooldown.getKey()}

    #def __init__(self, string, cooldown=10):
    #    super(Response, self).__init__(cooldown)
    #    self.string = string

    def respond(self, sender, message):
        print message.Message
        if self.cooldown.Consume():
            for m in self.string.split('\n'):
                sender.send_message(m)
                sleep(0.5)

    def __str__(self):
        return self.string + " " + str(self.cooldown)

    def __repr__(self):
        return str(self)


class CodeResponse(ResponseBase):
    def __init__(self, cooldown, func, *args):
        super(CodeResponse, self).__init__(cooldown)
        self.func = func
        self.args = args
        return

    def respond(self, sender, message):
        self.func(sender, message, self.args)
        return


class SoundResponse(ResponseBase):
    def __init__(self, soundFile, cooldown=10):
        super(SoundResponse, self).__init__(cooldown)
        self.soundFile = soundFile

    def respond(self, sender, message):
        pass

