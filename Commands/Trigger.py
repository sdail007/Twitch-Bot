from InvocationList import InvocationList
import re


class Trigger(object):
    def __init__(self, Text, ID=0):
        self.Triggered = InvocationList()
        self.ID = ID
        self.Text = Text

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
        if not self.Regex.match(message.Message):
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


class UserSpecificTrigger(Trigger):
    def __init__(self, text, users):
        super(UserSpecificTrigger, self).__init__(text)
        self.users = [user.lower() for user in users]
        return

    def invoke(self, sender, message):
        if message.Sender not in self.users:
            return
        super(UserSpecificTrigger, self).invoke(sender, message)
