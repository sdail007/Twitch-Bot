from CommandsCapability import *

print "hosttarget"
message = r':tmi.twitch.tv HOSTTARGET #fullgrowngaming :xxshawn 86'
iter = CommandsCapability.hosttarget.finditer(message)
print [m.groupdict() for m in iter]
print

print "hosttarget"
message = r':tmi.twitch.tv HOSTTARGET #fullgrowngaming :xxshawn'
iter = CommandsCapability.hosttarget.finditer(message)
print [m.groupdict() for m in iter]
print

print "hosttarget"
message = r':tmi.twitch.tv HOSTTARGET #fullgrowngaming :xxshawn'
iter = CommandsCapability.hosttarget.finditer(message)
print [m.groupdict() for m in iter]
print

print "hosttarget"
message = r':tmi.twitch.tv HOSTTARGET #fullgrowngaming :-'
iter = CommandsCapability.hosttarget.finditer(message)
print [m.groupdict() for m in iter]
print

print "notice"
message = r'@msg-id=slow_off :tmi.twitch.tv NOTICE #dallas :This room is no longer in slow mode.'
iter = CommandsCapability.notice.finditer(message)
print [m.groupdict() for m in iter]
print
