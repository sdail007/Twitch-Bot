from Cooldown import Cooldown
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

    def respond(self, message):
        return


class Response(ResponseBase):
    def __init__(self, connection, string, cooldown=10):
        super(Response, self).__init__(cooldown)
        self.connection = connection
        self.string = string

    def respond(self, message):
        print message.Message
        if self.cooldown.Consume():
            for m in self.string.split('\n'):
                self.connection.send_message(m)
                sleep(0.5)

    def __str__(self):
        return self.string + " " + str(self.cooldown)


class CodeResponse(ResponseBase):
    def __init__(self, cooldown, func, *args):
        super(CodeResponse, self).__init__(cooldown)
        self.func = func
        self.args = args
        return

    def respond(self, message):
        self.func(message, self.args)
        return


class SoundResponse(ResponseBase):
    def __init__(self, soundFile, cooldown=10):
        super(SoundResponse, self).__init__(cooldown)
        self.soundFile = soundFile

    def respond(self, message):
        pass
