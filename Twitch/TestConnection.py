from BotInterfaces.ChatInterface import *
from Twitch.ChatMessage import *
from Capabilities.TagsCapability import TagsCapability
from Capabilities.MembershipCapability import MembershipCapability
from Capabilities.CommandsCapability import CommandsCapability
from threading import Event
import re


class TestConnection(ChatInterface):
    wait = re.compile(r'^\$[Ww]ait\s?(?P<time>[0-9]*)?$')

    def __init__(self, file):
        super(TestConnection, self).__init__()
        with open(file) as w:
            self.lines = w.readlines()

        self.capabilities = [TagsCapability(), MembershipCapability(),
                             CommandsCapability()]
        return

    def start(self):

        for line in self.lines:
            Event().wait(1)
            line = line.rstrip('\r\n')
            match = self.wait.match(line)
            if match:
                tWait = 1
                if 'time' in match.groupdict():
                    tWait = int(match.groupdict()['time'])
                Event().wait(tWait)
            else:
                self.postMessage(line.rstrip('\r\n'))
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
