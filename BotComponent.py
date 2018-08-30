class BotComponent(object):
    def __init__(self, connection):
        self.connection = connection
        self.triggers = []
        return

    def shutdown(self):
        return

    def __del__(self):
        self.shutdown()
        return
