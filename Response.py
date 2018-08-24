#Embedded file name: C:\Users\Stephen\PycharmProjects\TwitchPlaysTicTacToe\Response.py
from Cooldown import Cooldown
from time import sleep

class Response(object):

    def __init__(self, connection, string, cooldown=10):
        self.connection = connection
        self.string = string
        if isinstance(cooldown, int):
            self.cooldown = Cooldown(cooldown)
        elif isinstance(cooldown, Cooldown):
            self.cooldown = cooldown
        else:
            raise TypeError('cooldown must be int or Cooldown')

    def addTrigger(self, trigger):
        trigger.Triggered.add(self.respond)

    def respond(self, message):
        print message.Message
        if self.cooldown.Consume():
            for m in self.string.split('\n'):
                self.connection.send_message(m)
                sleep(0.5)

    def __str__(self):
        return self.string + " " + str(self.cooldown)


class SoundResponse(Response):

    def __init__(self, soundFile, trigger):
        self.soundFile = soundFile
        self.trigger = trigger

    def respond(self, message):
        pass
