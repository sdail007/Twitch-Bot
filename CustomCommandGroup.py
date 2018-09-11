import os
import codecs
import json
import re

from Trigger import Trigger
from Cooldown import *
from Response import Response
from BotComponent import BotComponent


class CustomCommandGroup(BotComponent):
    def __init__(self, folder, connection):
        super(CustomCommandGroup, self).__init__(connection)

        self.folder = folder
        self.cooldowns = []
        self.responses = []
        provider = CooldownProvider(self.cooldowns)

        file = os.path.join(self.folder, "Triggers.json")
        with codecs.open(file, encoding="utf-8-sig", mode="r") as f:
            for trigger in json.load(f, encoding="utf-8"):
                self.triggers.append(Trigger.fromSettings(trigger))

        file = os.path.join(self.folder, "Cooldowns.json")

        with codecs.open(file, encoding="utf-8-sig", mode="r") as f:
            for cd in json.load(f, encoding="utf-8"):
                self.cooldowns.append(Cooldown.fromSettings(cd))

        file = os.path.join(self.folder, "Responses.json")

        with codecs.open(file, encoding="utf-8-sig", mode="r") as f:
            for response in json.load(f, encoding="utf-8"):
                self.responses.append(Response.fromSettings(response, provider))

        file = os.path.join(self.folder, "TriggersToResponses.json")
        with codecs.open(file, encoding="utf-8-sig", mode="r") as f:
            for link in json.load(f, encoding="utf-8"):
                responseKey = link["Response"]
                triggerKey = link["Trigger"]
                r = next((x for x in self.responses if x.ID == int(responseKey)),
                     None)
                t = next((x for x in self.triggers if x.ID == int(triggerKey)),
                     None)
                r.addTrigger(t)

    def save(self):
        file = os.path.join(self.folder, "Triggers.json")
        with codecs.open(file, encoding="utf-8-sig", mode="w+") as f:
            output = [t.dumpAsDict() for t in self.triggers]
            json.dump(output, f, encoding="utf-8", indent=4,
                      sort_keys=True)

        file = os.path.join(self.folder, "Cooldowns.json")
        with codecs.open(file, encoding="utf-8-sig", mode="w+") as f:
            output = [t.dumpAsDict() for t in self.cooldowns]
            json.dump(output, f, encoding="utf-8", indent=4,
                      sort_keys=True)

        file = os.path.join(self.folder, "Responses.json")
        with codecs.open(file, encoding="utf-8-sig", mode="w+") as f:
            output = [t.dumpAsDict() for t in self.responses]
            json.dump(output, f, encoding="utf-8", indent=4,
                      sort_keys=True)
            '''
        file = os.path.join(self.folder, "TriggersToResponses.json")
        with codecs.open(file, encoding="utf-8-sig", mode="w+") as f:
            json.dump(self.triggers, f, encoding="utf-8", indent=4,
                      sort_keys=True)
                      '''
        return

    def shutdown(self):
        self.save()
        return
