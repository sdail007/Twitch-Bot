import os
import json
import codecs


def GetEevee(settings_file):
    with codecs.open(settings_file, encoding="utf-8-sig", mode="r") as f:
        return json.load(f, encoding="utf-8")

def save(self):
    with codecs.open(self.settings_file, encoding="utf-8-sig",
                     mode="w+") as f:
        json.dump(self.Values, f, encoding="utf-8", indent=4,
                  sort_keys=True)
