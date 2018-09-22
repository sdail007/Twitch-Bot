import re


class MembershipCapability(object):

    join = re.compile(r':(?P<user>[^;]+)!(?P=user)@(?P=user)'
                      r'\.tmi\.twitch\.tv '
                      r'JOIN '
                      r'#(?P<channel>[^;]+)')

    mode = re.compile(r':jtv MODE '
                      r'#(?P<channel>[^;]+) '
                      r'(?P<change>[-+]o) '
                      r'(?P<user>[^;]+)')

    names = re.compile(r':(?P<user>[^;]+).tmi.twitch.tv 353 '
                       r'(?P=user) = #(?P<channel>[^;]+) '
                       r':(?P<names>.+)')

    part = re.compile(r':(?P<user>[^;]+)!(?P=user)@(?P=user)'
                      r'\.tmi\.twitch\.tv '
                      r'PART '
                      r'#(?P<channel>[^;]+)')
