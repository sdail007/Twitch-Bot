from InvocationList import InvocationList
import re


class Trigger(object):
    def __init__(self, text):
        self.text = text
        self.Triggered = InvocationList()

    def invoke(self, sender, message):
        parts = message.Message.split(' ', 1)
        if parts[0].lower() != self.text.lower():
            return

        message.Command = parts[0]

        if len(parts) > 1:
            message.Params = parts[1]

        self.Triggered.invoke(sender, message)

    def __str__(self):
        return self.text


class RegexTrigger(Trigger):
    def __init__(self, text):
        super(RegexTrigger, self).__init__(text)
        self.Regex = re.compile(text)

    def invoke(self, sender, message):
        if not re.match(message.Message):
            return
        self.Triggered.invoke(sender, message)
