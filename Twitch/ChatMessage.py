import re


class ChatMessage(object):
    regex = re.compile(r'(?P<Sender>.*)!(.*)\b(?P<MessageType>\S+)\b'
                       r' #(?P<Channel>.*)')

    def __init__(self, string):
        if not isinstance(string, str):
            raise TypeError('string must be set to an str')
        stringParts = string.split(' :')
        self.Tags = stringParts[0]

        if len(stringParts) < 2:
            return

        my_dude = ChatMessage.regex.match(stringParts[1])

        if not my_dude:
            return

        parts = my_dude.groupdict()
        self.Sender = parts['Sender']
        self.MessageType = parts['MessageType']
        self.Channel = parts['Channel']
        self.Message = stringParts[2]

    def __str__(self):
        return self.Sender + ': ' + self.Message
