import re

class CommandsCapability(object):
    hosttarget = re.compile(r':tmi.twitch.tv HOSTTARGET '
                            r'#(?P<hostingChannel>\S+) '
                            r':(?P<channel>\S+)'
                            r'( (?P<numviewers>\d+))?')

    notice = re.compile(r'@msg-id=(?P<msgid>\S+) '
                        r':tmi.twitch.tv '
                        r'NOTICE #(?P<channel>\S+) '
                        r':(?P<message>.+)')

    reconnect = re.compile(r'RECONNECT')

