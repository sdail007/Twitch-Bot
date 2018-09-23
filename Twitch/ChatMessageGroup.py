class TwitchCapability(object):
    def __init__(self):
        self.subscriptionmessage = None
        self.regexes = {}
        return

    def Parse(self, text):
        for key in self.regexes:
            match = self.regexes[key].match(text)
            if match:
                print key
                return match.groupdict()
