from Twitch.Capabilities.MembershipCapability import *

print "join"
message = r':ronni!ronni@ronni.tmi.twitch.tv JOIN #dallas'
iter = MembershipCapability.join.finditer(message)
print [m.groupdict() for m in iter]
print

print "mode+"
message = r':jtv MODE #dallas +o ronni'
iter = MembershipCapability.mode.finditer(message)
print [m.groupdict() for m in iter]
print

print "mode-"
message = r':jtv MODE #dallas -o ronni'
iter = MembershipCapability.mode.finditer(message)
print [m.groupdict() for m in iter]
print

print "names"
message = r':ronni.tmi.twitch.tv 353 ronni = #dallas :ronni fred wilma'
iter = MembershipCapability.names.finditer(message)
print [m.groupdict() for m in iter]
print

print "part"
message = r':ronni!ronni@ronni.tmi.twitch.tv PART #dallas'
iter = MembershipCapability.part.finditer(message)
print [m.groupdict() for m in iter]
print
