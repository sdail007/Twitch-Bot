from InvocationList import InvocationList


class ChatInterface(object):
    def __init__(self):
        self.MessageReceived = InvocationList()
        self.EventReceived = InvocationList()
        return

    def send_message(self, message):
        return

    def stop(self):
        return

    def start(self):
        return
