import re
from Twitch.ChatMessageGroup import TwitchCapability


class MembershipCapability(TwitchCapability):

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
        super(MembershipCapability, self).\
            __init__(r'CAP REQ :twitch.tv/membership')
        self.regexes["join"] = MembershipCapability.join
        self.regexes["mode"] = MembershipCapability.mode
        self.regexes["names"] = MembershipCapability.names
        self.regexes["part"] = MembershipCapability.part
        return
