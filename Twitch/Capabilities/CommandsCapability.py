import re
from Twitch.ChatMessageGroup import TwitchCapability


class CommandsCapability(TwitchCapability):
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
        super(CommandsCapability, self).__init__(r'CAP REQ :twitch.tv/tags')
        self.regexes["hosttarget"] = CommandsCapability.hosttarget
        self.regexes["notice"] = CommandsCapability.notice
        self.regexes["reconnect"] = CommandsCapability.reconnect
        return
