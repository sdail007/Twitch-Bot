import re
from Twitch.ChatMessageGroup import TwitchCapability


class TagsCapability(TwitchCapability):
    clearchat = re.compile(r':tmi\.twitch\.tv CLEARCHAT #(?P<channel>.+) '
                           r':(?P<user>.+) '
                           r'@(ban-duration=(?P<banduration>[^;]+);)?'
                           r'ban-reason=(?P<banreason>[^;]+) '
                           r':tmi\.twitch\.tv '
                           r'(?P<command>CLEARCHAT) '
                           r'#(?P=channel) '
                           r':(?P=user)')

    globaluserstate = re.compile(r'@badge-info=(?P<badgeinfo>[^;]*);'
                                 r'badges=(?P<badges>[^;]*);'
                                 r'color=(?P<color>[^;]*);'
                                 r'display-name=(?P<displayname>[^;]*);'
                                 r'emote-sets=(?P<emotesets>[^;]+);'
                                 r'turbo=(?P<turbo>[^;]+);'
                                 r'user-id=(?P<userid>[^;]+);'
                                 r'user-type=(?P<usertype>.+) '
                                 r':tmi\.twitch\.tv '
                                 r'(?P<command>GLOBALUSERSTATE)')

    privmsg = re.compile(r'@badge-info=(?P<badgeinfo>[^;]*);'
                         r'badges=(?P<badges>[^;]*);'
                         r'(bits=(?P<bits>[^;]*);)?'
                         r'color=(?P<color>[^;]*);'
                         r'display-name=(?P<displayname>[^;]*);'
                         r'(emote-only=(?P<emoteonly>.);)?'
                         r'emotes=(?P<emotes>[^;]*);'
                         r'(flags=(?P<flags>[^;]*);)?'
                         r'id=(?P<idofmsg>[^;]+);'
                         r'mod=(?P<mod>[^;]+);'
                         r'room-id=(?P<roomid>[^;]+);'
                         r'subscriber=(?P<subscriber>[^;]+);'
                         r'tmi-sent-ts=(?P<timestamp>[^;]+);'
                         r'turbo=(?P<turbo>[^;]+);'
                         r'user-id=(?P<userid>[^;]+);'
                         r'user-type=(?P<usertype>[^;]*) '
                         r':(?P<user>[^;]+)!(?P=user)@(?P=user)'
                         r'\.tmi\.twitch\.tv '
                         r'(?P<command>PRIVMSG) '
                         r'#(?P<channel>[^;]+) '
                         r':(?P<message>[^;]+)')

    roomstate = re.compile(r'@(broadcaster-lang=(?P<broadcasterlang>[^;]+))?;?'
                           r'(r9k=(?P<r9k>[^;]+))?;?'
                           r'(slow=(?P<slow>[^;]+))?;?'
                           r'(subs-only=(?P<subsonly>.+))? '
                           r':tmi\.twitch\.tv '
                           r'(?P<command>ROOMSTATE) '
                           r'#(?P<channel>.+)')

    subnotice = re.compile(r'@badge-info=(?P<badgeinfo>[^;]*);'
                           r'badges=(?P<badges>[^;]*);'
                           r'color=(?P<color>[^;]+);'
                           r'display-name=(?P<displayname>[^;]+);'
                           r'emotes=(?P<emotes>[^;]*);'
                           r'id=(?P<idofmsg>[^;]+);'
                           r'login=(?P<user>[^;]+);'
                           r'mod=(?P<mod>[^;]+);'
                           r'msg-id=(?P<msgid>[^;]+);'                          
                           r'msg-param-months=(?P<months>[^;]+);'
                           r'msg-param-sub-plan=(?P<subplan>[^;]+);'
                           r'msg-param-sub-plan-name=(?P<subplanname>[^;]+);'
                           r'room-id=(?P<roomid>[^;]+);'
                           r'subscriber=(?P<subscriber>[^;]+);'
                           r'system-msg=(?P<systemmsg>[^;]+);'
                           r'tmi-sent-ts=(?P<timestamp>[^;]+);'
                           r'turbo=(?P<turbo>[^;]+);'
                           r'user-id=(?P<userid>[^;]+);'
                           r'user-type=(?P<usertype>.+) '
                           r':tmi\.twitch\.tv '
                           r'(?P<command>USERNOTICE) '
                           r'#(?P<channel>.+) '
                           r':(?P<message>.+)')

    giftnotice = re.compile(r'@badge-info=(?P<badgeinfo>[^;]*);'
                            r'badges=(?P<badges>[^;]*);'
                            r'color=(?P<color>[^;]*);'
                            r'display-name=(?P<displayname>[^;]+);'
                            r'emotes=(?P<emotes>[^;]*);'
                            r'id=(?P<idofmsg>[^;]+);'
                            r'login=(?P<user>[^;]+);'
                            r'mod=(?P<mod>[^;]+);'
                            r'msg-id=(?P<msgid>[^;]+);'
                            r'msg-param-months=(?P<msgparammonths>[^;]+);'
                            r'msg-param-recipient-display-name=(?P<recipientdisplayname>[^;]+);'
                            r'msg-param-recipient-id=(?P<recipientid>[^;]+);'
                            r'msg-param-recipient-name=(?P<recipientusername>[^;]+);'
                            r'msg-param-sub-plan-name=(?P<subplanname>[^;]+);'
                            r'msg-param-sub-plan=(?P<subplan>[^;]+);'
                            r'room-id=(?P<roomid>[^;]+);'
                            r'subscriber=(?P<subscriber>[^;]+);'
                            r'system-msg=(?P<systemmsg>[^;]+);'
                            r'tmi-sent-ts=(?P<timestamp>[^;]+);'
                            r'turbo=(?P<turbo>[^;]+);'
                            r'user-id=(?P<userid>[^;]+);'
                            r'user-type=(?P<usertype>.*)' 
                            r':tmi\.twitch\.tv '
                            r'(?P<command>USERNOTICE) '
                            r'#(?P<channel>.+)'
                            r'( :(?P<message>.+))?')

    raidnotice = re.compile(r'@badge-info=(?P<badgeinfo>[^;]*);'
                            r'badges=(?P<badges>[^;]*);'
                            r'color=(?P<color>[^;]*);'
                            r'display-name=(?P<displayname>[^;]*);'
                            r'emotes=(?P<emotes>[^;]*);'
                            r'id=(?P<idofmsg>[^;]+);'
                            r'login=(?P<user>[^;]+);'
                            r'mod=(?P<mod>[^;]+);'
                            r'msg-id=(?P<msgid>[^;]+);'
                            r'msg-param-displayName=(?P<raidDisplayName>[^;]+);'
                            r'msg-param-login=(?P<raidChannel>[^;]+);'
                            r'msg-param-viewerCount=(?P<raidViewerCount>[^;]+);'
                            r'room-id=(?P<roomid>[^;]+);'
                            r'subscriber=(?P<subscriber>[^;]+);'
                            r'system-msg=(?P<systemmsg>[^;]+);'
                            r'tmi-sent-ts=(?P<timestamp>[^;]+);'
                            r'turbo=(?P<turbo>[^;]+);'
                            r'user-id=(?P<userid>[^;]+);'
                            r'user-type=(?P<usertype>.*) '
                            r':tmi\.twitch\.tv '
                            r'(?P<command>USERNOTICE) '
                            r'#(?P<channel>.+)'
                            r'( :(?P<message>.+))?')

    ritualnotice = re.compile(r'@badge-info=(?P<badgeinfo>[^;]*);'
                              r'badges=(?P<badges>[^;]*);'
                              r'color=(?P<color>[^;]*);'
                              r'display-name=(?P<displayname>[^;]*);'
                              r'emotes=(?P<emotes>[^;]*);'
                              r'id=(?P<idofmsg>[^;]+);'
                              r'login=(?P<user>[^;]+);'
                              r'mod=(?P<mod>[^;]+);'
                              r'msg-id=(?P<msgid>[^;]+);'
                              r'msg-param-ritual-name=(?P<ritualName>[^;]+);'
                              r'room-id=(?P<roomid>[^;]+);'
                              r'subscriber=(?P<subscriber>[^;]+);'
                              r'system-msg=(?P<systemmsg>[^;]+);'
                              r'tmi-sent-ts=(?P<timestamp>[^;]+);'
                              r'turbo=(?P<turbo>[^;]+);'
                              r'user-id=(?P<userid>[^;]+);'
                              r'user-type=(?P<usertype>.*) '
                              r':tmi\.twitch\.tv '
                              r'(?P<command>USERNOTICE) '
                              r'#(?P<channel>.+)'
                              r'( :(?P<message>.+))?')

    userstate = re.compile(r'@badge-info=(?P<badgeinfo>[^;]*);'
                           r'badges=(?P<badges>[^;]*);'
                           r'color=(?P<color>[^;]*);'
                           r'display-name=(?P<displayname>[^;]*);'
                           r'emote-sets=(?P<emotes>[^;]*);'
                           r'mod=(?P<mod>[^;]*);'
                           r'subscriber=(?P<subscriber>[^;]*);'
                           r'turbo=(?P<turbo>[^;]*);'
                           r'user-type=(?P<usertype>.*) '
                           r':tmi\.twitch\.tv '
                           r'(?P<command>USERSTATE) '
                           r'#(?P<channel>[^;]*)')

    def __init__(self):
        super(TagsCapability, self).__init__(r'CAP REQ :twitch.tv/tags')
        self.regexes["privmsg"] = TagsCapability.privmsg
        self.regexes["clearchat"] = TagsCapability.clearchat
        self.regexes["globaluserstate"] = TagsCapability.globaluserstate
        self.regexes["roomstate"] = TagsCapability.roomstate
        self.regexes["subnotice"] = TagsCapability.subnotice
        self.regexes["giftnotice"] = TagsCapability.giftnotice
        self.regexes["raidnotice"] = TagsCapability.raidnotice
        self.regexes["ritualnotice"] = TagsCapability.ritualnotice
        self.regexes["userstate"] = TagsCapability.userstate
        return

'''
    def Parse(self, text):
        for key in self.regexes:
            match = self.regexes[key].match(text)
            if match:
                print key
                return match.groupdict()
'''