import os
import codecs
import json
import importlib


class ComponentLoader:
    def __init__(self, settings_dir):
        self.settings_dir = settings_dir
        #insert settings_dir at beginning of os path
        os.environ["PATH"] = self.settings_dir + os.pathsep + os.environ["PATH"]
        return

    def get_settings(self):
        setupfile = os.path.join(self.settings_dir, "setup.json")
        with codecs.open(setupfile, encoding="utf-8-sig", mode="r") as f:
            setup = json.load(f, encoding="utf-8")

        return setup

    def get_components(self):
        setup = self.get_settings()
        names = setup['components'].keys()
        return names

    def activate_all(self):
        components = []

        setup = self.get_settings()

        for componentSetting in setup['components'].values():
            module_name = str(componentSetting['type'])
            file = str(componentSetting['file'])

            component = self.create_component(module_name, file)

            components.append(component)
        return components

    def activate_component(self, componentName):
        setup = self.get_settings()
        componentDefinition = setup['components'][componentName]

        module_name = str(componentDefinition['type'])
        file = str(componentDefinition['file'])

        component = self.create_component(module_name, file)
        return component

    def create_component(self, module_name, file):
        module = importlib.import_module(module_name)
        classname = str(module_name.split('.')[-1])
        myClass = getattr(module, classname)

        path = os.path.join(self.settings_dir, file)

        component = myClass(path)
        return component

