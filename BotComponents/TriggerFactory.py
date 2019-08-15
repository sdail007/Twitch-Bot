from Commands.Trigger import *


class TriggerFactory:
    def __init__(self):
        self.Triggers = []
        return

    def create_trigger(self, text):
        trigger = Trigger(text)
        self.Triggers.append(trigger)
        return trigger

    def create_regex_trigger(self, regex):
        trigger = RegexTrigger(regex)
        self.Triggers.append(trigger)
        return trigger

