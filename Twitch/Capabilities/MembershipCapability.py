import re


class MembershipCapability(object):

    join = re.compile(r':(?P<user>[^;]+)!(?P=user)@(?P=user)'
                      r'\.tmi\.twitch\.tv '
                      r'(?P<command>JOIN) '
                      r'#(?P<channel>[^;]+)')

    mode = re.compile(r':jtv '
                      r'(?P<command>MODE) '
                      r'#(?P<channel>[^;]+) '
                      r'(?P<change>[-+]o) '
                      r'(?P<user>[^;]+)')

    names = re.compile(r':(?P<user>[^;]+).tmi.twitch.tv '
                       r'(?P<command>353) '
                       r'(?P=user) = #(?P<channel>[^;]+) '
                       r':(?P<names>.+)')

    part = re.compile(r':(?P<user>[^;]+)!(?P=user)@(?P=user)'
                      r'\.tmi\.twitch\.tv '
                      r'(?P<command>PART) '
                      r'#(?P<channel>[^;]+)')

    def __init__(self):
        self.subscriptionmessage = r'CAP REQ :twitch.tv/membership'
        self.regexes = {"join": MembershipCapability.join,
                        "mode": MembershipCapability.mode,
                        "names": MembershipCapability.names,
                        "part": MembershipCapability.part,
                        }
        return

    def Parse(self, text):
        for key in self.regexes:
            match = self.regexes[key].match(text)
            if match:
                print key
                return match.groupdict()

