from BotComponents.BotComponentAdaptor import *

class BotInstance(object):
    def __init__(self, connection):
        self.connection = connection
        self.components = []

    def start(self):
        self.connection.start()

        for component in self.components:
            component.enable(self.connection)
        return

    def add_component(self, component):
        adaptor = BotComponentAdaptor(component)
        self.components.append(adaptor)
        return

    def shutdown(self):
        self.connection.stop()
        for component in self.components:
            component.disable()

    def send_message(self, msg):
        self.connection.send_message(msg)

    def __del__(self):
        self.shutdown()
