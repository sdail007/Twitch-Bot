import os
import codecs
import json

from Commands.Cooldown import *
from Commands.Response import Response
from BotInterfaces.BotComponent import BotComponent


class CustomCommandGroup(BotComponent):
    def __init__(self, folder):
        super(CustomCommandGroup, self).__init__()
        self.folder = folder

        self.triggers = {}
        self.responses = {}
        self.cooldowns = {}
        return

    def initialize(self, adaptor):
        self.cooldowns.clear()
        self.triggers.clear()
        self.responses.clear()

        file = os.path.join(self.folder, "Triggers.json")
        with codecs.open(file, encoding="utf-8-sig", mode="r") as f:
            for trigger in json.load(f, encoding="utf-8"):
                trigger_id = trigger["ID"]
                trigger_text = trigger["Text"]
                t = adaptor.trigger_factory.create_trigger(trigger_text)
                self.triggers[trigger_id] = t

        file = os.path.join(self.folder, "Cooldowns.json")

        with codecs.open(file, encoding="utf-8-sig", mode="r") as f:
            for cd in json.load(f, encoding="utf-8"):
                alias = cd["Alias"]
                seconds = cd["Seconds"]
                cooldown = Cooldown(seconds, alias)
                self.cooldowns[alias] = cooldown

        file = os.path.join(self.folder, "Responses.json")

        with codecs.open(file, encoding="utf-8-sig", mode="r") as f:
            for response in json.load(f, encoding="utf-8"):
                ID = response["ID"]
                string = response["text"]
                cooldown = response["cooldown"]

                if isinstance(cooldown, basestring):
                    cd = self.cooldowns[cooldown]
                elif isinstance(cooldown, int):
                    cd = Cooldown(cooldown)
                else:
                    raise TypeError

                r = Response(string, cd)
                self.responses[ID] = r

        file = os.path.join(self.folder, "TriggersToResponses.json")
        with codecs.open(file, encoding="utf-8-sig", mode="r") as f:
            for link in json.load(f, encoding="utf-8"):
                triggerKey = link["Trigger"]
                responseKey = link["Response"]
                t = self.triggers[triggerKey]
                r = self.responses[responseKey]
                r.addTrigger(t)
        return

    def save(self):
        file = os.path.join(self.folder, "Triggers.json")
        with codecs.open(file, encoding="utf-8-sig", mode="w+") as f:
            output = [CustomCommandGroup.SerializeTrigger(tid, trigger)
                      for tid, trigger in self.triggers.items()]
            json.dump(output, f, encoding="utf-8", indent=4,
                      sort_keys=True)

        file = os.path.join(self.folder, "Cooldowns.json")
        with codecs.open(file, encoding="utf-8-sig", mode="w+") as f:
            output = [CustomCommandGroup.SerializeCooldown(id, cooldown)
                      for id, cooldown in self.cooldowns.items()]
            json.dump(output, f, encoding="utf-8", indent=4,
                      sort_keys=True)

        file = os.path.join(self.folder, "Responses.json")
        with codecs.open(file, encoding="utf-8-sig", mode="w+") as f:
            output = [CustomCommandGroup.SerializeResponse(id, response)
                      for id, response in self.responses.items()]
            json.dump(output, f, encoding="utf-8", indent=4,
                      sort_keys=True)
        return

    def shutdown(self):
        self.save()
        return

    @classmethod
    def SerializeTrigger(cls, trigger_id, trigger):
        return {"ID": trigger_id, "Text": trigger.Text}

    @classmethod
    def SerializeCooldown(cls, alias, cooldown):
        return {"Alias": alias, "Seconds": cooldown.cooldown}

    @classmethod
    def SerializeResponse(cls, response_id, response):
        return {"ID": response_id, "text": response.string,
                "cooldown": response.cooldown.getKey()}
