import os
import json
import codecs


class EeveeSettings(object):
    def __init__(self, settings_file):
        with codecs.open(settings_file, encoding="utf-8-sig", mode="r") as f:
            self.__dict__ = json.load(f, encoding="utf-8")
        self.settings_file = settings_file

    def save(self):
        with codecs.open(self.settings_file, encoding="utf-8-sig",
                         mode="w+") as f:
            json.dump(self.__dict__, f, encoding="utf-8", indent=4,
                      sort_keys=True)
