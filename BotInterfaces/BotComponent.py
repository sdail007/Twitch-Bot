class BotComponent(object):
    def __init__(self):
        self.adaptor = None
        return

    def initialize(self, adaptor):
        self.adaptor = adaptor
        return

    def shutdown(self):
        return

    def __del__(self):
        return
