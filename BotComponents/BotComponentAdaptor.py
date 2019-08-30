from TriggerFactory import TriggerFactory


class BotComponentAdaptor:
    def __init__(self, component):
        self.trigger_factory = None
        self.component = component
        self.connection = None  #todo: remove
        self.enabled = None
        return

    def MessageReceived(self, sender, msg):
        for trigger in self.trigger_factory.Triggers:
            trigger.invoke(sender, msg)

    def send_message(self, message):
        if self.enabled:
            self.connection.send_message(message)
        return

    def enable(self, connection):
        if self.enabled:
            return

        self.trigger_factory = TriggerFactory()

        self.connection = connection
        self.enabled = True

        self.component.initialize(self)
        connection.MessageReceived.add(self.MessageReceived)
        return

    def disable(self):
        if not self.enabled:
            return

        print 'enabled {0}'.format(str(type(self.component)))

        self.enabled = False
        self.connection.MessageReceived.remove(self.MessageReceived)

        #this should only happen when deleted
        self.component.shutdown()
        return

    def __del__(self):
        del self.component
        return

