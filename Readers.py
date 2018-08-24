import os
import codecs
import json
import re

from Trigger import Trigger
from Cooldown import Cooldown
from Response import Response

class Triggers(object):
    def __init__(self, folder):
        file = os.path.join(folder, "Triggers.json")

        with codecs.open(file, encoding="utf-8-sig", mode="r") as f:
            stuff = json.load(f, encoding="utf-8")

        self.Triggers = {"key": "value"}
        for key, value in stuff.items():
            t = Trigger(value)
            self.Triggers[key] = t
            print "triggers-loaded: ",t
        return


class Cooldowns(object):
    def __init__(self, folder):
        file = os.path.join(folder, "Cooldowns.json")

        with codecs.open(file, encoding="utf-8-sig", mode="r") as f:
            stuff = json.load(f, encoding="utf-8")

        self.Cooldowns = {"key": "value"}
        for key, value in stuff.items():
            c = Cooldown(value["Timeout"])
            self.Cooldowns[key] = c
            print "cooldowns-loaded: ", c
        return


class Responses(object):
    fkregex = re.compile(r"^\{(?P<cooldown>\S+)\}$")

    def __init__(self, folder, connection, cooldowns):
        file = os.path.join(folder, "Responses.json")

        with codecs.open(file, encoding="utf-8-sig", mode="r") as f:
            stuff = json.load(f, encoding="utf-8")

        self.Responses = {"key": "value"}
        for key, value in stuff.items():
            match = Responses.fkregex.match(value["cooldown"])
            if match:
                fk = match.groupdict()["cooldown"]
                cooldown = cooldowns.Cooldowns[fk]
            else:
                cooldown = int(value["cooldown"])

            r = Response(connection, value["text"], cooldown)
            self.Responses[key] = r
            print "responses-loaded: ",  r
        return


class Links(object):
    def __init__(self, folder):
        file = os.path.join(folder, "TriggersToResponses.json")
        with codecs.open(file, encoding="utf-8-sig", mode="r") as f:
            self.__dict__ = json.load(f, encoding="utf-8")

    def __getitem__(self, item):
        return self.__dict__[item]

    def __iter__(self):
        return self.__dict__

