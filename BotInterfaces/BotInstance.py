from BotComponents.BotComponentAdaptor import *


class BotInstance(object):
    def __init__(self):
        self.running = False
        self.connection = None
        self.components = []

    def set_connection(self, connection):
        self.connection = connection

    def start(self):
        if self.connection is None:
            return

        self.running = True
        self.connection.start()

        for component in self.components:
            component.enable(self.connection)
        return

    def stop(self):
        if not self.running:
            return

        self.running = False

        for component in self.components:
            component.disable()

        self.connection.stop()

    def add_component(self, component):
        adaptor = BotComponentAdaptor(component)
        self.components.append(adaptor)

        if self.running:
            adaptor.enable(self.connection)
        return

    def send_message(self, msg):
        self.connection.send_message(msg)

    def __del__(self):
        self.stop()

