from InvocationList import InvocationList
import re


class Trigger(object):
    @classmethod
    def fromSettings(cls, settings):
        ID = settings["ID"]
        Text = settings["Text"]
        return cls(Text, ID)

    def __init__(self, Text, ID=0):
        self.Triggered = InvocationList()
        self.ID = ID
        self.Text = Text

    def dumpAsDict(self):
        return {"ID": self.ID, "Text": self.Text}

    def invoke(self, sender, message):
        parts = message.Message.split(' ', 1)
        if parts[0].lower() != self.Text.lower():
            return

        message.Command = parts[0]

        if len(parts) > 1:
            message.Params = parts[1]

        self.Triggered.invoke(sender, message)

    def __str__(self):
        return self.Text

    def __repr__(self):
        return str(self)


class RegexTrigger(Trigger):
    def __init__(self, text):
        super(RegexTrigger, self).__init__(text)
        self.Regex = re.compile(text)

    def invoke(self, sender, message):
        if not re.match(message.Message):
            return
        self.Triggered.invoke(sender, message)


class ContainsTrigger(Trigger):
    def __init__(self, text):
        super(ContainsTrigger, self).__init__(text)
        return

    def invoke(self, sender, message):
        if self.Text not in message.Message:
            return
        self.Triggered.invoke(sender, message)
