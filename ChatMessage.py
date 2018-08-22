#Embedded file name: C:\Users\Stephen\PycharmProjects\TwitchPlaysTicTacToe\ChatMessage.py
import re
from InvocationList import InvocationList

class ChatMessage(object):
    MessageReceived = InvocationList()
    regex = re.compile('(?P<Sender>.*)!(.*)\\b(?P<MessageType>\\S+)\\b #(?P<Channel>.*)')

    def __init__(self, string):
        if not isinstance(string, str):
            raise TypeError('string must be set to an str')
        stringParts = string.split(' :')
        self.Tags = stringParts[0]
        my_dude = ChatMessage.regex.match(stringParts[1])
        parts = my_dude.groupdict()
        self.Sender = parts['Sender']
        self.MessageType = parts['MessageType']
        self.Channel = parts['Channel']
        self.Message = stringParts[2]

    def __str__(self):
        return self.Sender + ': ' + self.Message

    def invoke(self):
        ChatMessage.MessageReceived.invoke(self)


class PrivMsg(ChatMessage):

    def __init__(self, string):
        pass

    def invoke(self):
        pass
