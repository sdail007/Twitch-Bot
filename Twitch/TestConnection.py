from Commands.ChatInterface import *
from Twitch.ChatMessage import *
from Capabilities.TagsCapability import TagsCapability
from Capabilities.MembershipCapability import MembershipCapability
from Capabilities.CommandsCapability import CommandsCapability
from threading import Event


class TestConnection(ChatInterface):
    def __init__(self, file):
        super(TestConnection, self).__init__()
        with open(file) as w:
            self.lines = w.readlines()

        self.capabilities = [TagsCapability(), MembershipCapability(),
                             CommandsCapability()]
        return

    def start(self):
        Event().wait(10)    # pretend to connect lol

        for line in self.lines:
            self.postMessage(line)
        return

    def postMessage(self, message):
        stuff = None
        for capability in self.capabilities:
            stuff = capability.Parse(message)
            if stuff is not None:
                break

        if stuff is None:
            print 'UNABLE TO PARSE {}'.format(message)
            return

        if stuff['command'] == 'PRIVMSG':
            # print message
            # Decode message and propogate to listeners
            chat_message = ChatMessage(message)
            self.MessageReceived.invoke(self, chat_message)

        self.EventReceived.invoke(self, stuff)
