#Embedded file name: C:\Users\Stephen\PycharmProjects\TwitchPlaysTicTacToe\Trigger.py
from InvocationList import InvocationList
import re

class Trigger(object):
    Triggers = []

    def __init__(self, text):
        self.text = text
        self.Triggered = InvocationList()
        Trigger.Triggers.append(self)

    def invoke(self, message):
        if message.Message != self.text:
            return
        self.Triggered.invoke(message)

    def __del__(self):
        Trigger.Triggers.remove(self)


class RegexTrigger(Trigger):

    def __init__(self, text):
        super(text)
        self.Regex = re.compile(text)

    def invoke(self, message):
        if not re.match(message.Message):
            return
        self.Triggered.invoke(message)
