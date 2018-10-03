class TwitchCapability(object):
    def __init__(self, subMessage):
        self.subscriptionmessage = subMessage
        self.regexes = {}
        return

    def Parse(self, text):
        for key in self.regexes:
            match = self.regexes[key].match(text)
            if match:
                return match.groupdict()
