import re


class CommandsCapability(object):
    hosttarget = re.compile(r':tmi.twitch.tv '
                            r'(?P<command>HOSTTARGET) '
                            r'#(?P<hostingChannel>\S+) '
                            r':(?P<channel>\S+)'
                            r'( (?P<numviewers>\d+))?')

    notice = re.compile(r'@msg-id=(?P<msgid>\S+) '
                        r':tmi.twitch.tv '
                        r'(?P<command>NOTICE) '
                        r'#(?P<channel>\S+) '
                        r':(?P<message>.+)')

    reconnect = re.compile(r'(?P<command>RECONNECT)')

    def __init__(self):
        self.subscriptionmessage = r'CAP REQ :twitch.tv/tags'
        self.regexes = {"hosttarget": CommandsCapability.hosttarget,
                        "notice": CommandsCapability.notice,
                        "reconnect": CommandsCapability.reconnect,
                        }
        return

    def Parse(self, text):
        for key in self.regexes:
            match = self.regexes[key].match(text)
            if match:
                print key
                return match.groupdict()
