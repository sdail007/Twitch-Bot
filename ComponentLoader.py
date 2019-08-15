import os
import codecs
import json
import importlib


class ComponentLoader:
    def __init__(self):
        return

    @classmethod
    def get_components(cls, settings_dir):
        components = []

        setupfile = os.path.join(settings_dir, "setup.json")
        with codecs.open(setupfile, encoding="utf-8-sig", mode="r") as f:
            setup = json.load(f, encoding="utf-8")

            for componentSetting in setup['components']:
                # Get ClassType
                module_name = str(componentSetting['type'])
                module = importlib.import_module(module_name)
                classname = str(module_name.split('.')[-1])
                myClass = getattr(module, classname)

                # Get settings file
                file = str(componentSetting['file'])
                path = os.path.join(settings_dir, file)

                component = myClass(path)

                components.append(component)
        return components

