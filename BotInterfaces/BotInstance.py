from BotComponents.BotComponentAdaptor import *

class BotInstance(object):
    def __init__(self):
        self.running = False
        self.connection = None
        self.components = []

    def start(self, connection):
        self.running = True
        self.connection = connection
        self.connection.start()

        for component in self.components:
            component.enable(self.connection)
        return

    def add_component(self, component):
        adaptor = BotComponentAdaptor(component)
        self.components.append(adaptor)

        if self.running:
            component.enable(self.connection)
        return

    def shutdown(self):
        self.running = False
        self.connection.stop()
        for component in self.components:
            component.disable()

    def send_message(self, msg):
        self.connection.send_message(msg)

    def __del__(self):
        self.shutdown()

