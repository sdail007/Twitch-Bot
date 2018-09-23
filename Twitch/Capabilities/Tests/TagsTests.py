from Twitch.Capabilities.TagsCapability import *

print "clear chat"
clearchatMessage = r':tmi.twitch.tv CLEARCHAT #dallas :ronni @ban-reason=Follow\sthe\srules :tmi.twitch.tv CLEARCHAT #dallas :ronni'
iter = TagsCapability.clearchat.finditer(clearchatMessage)
print [m.groupdict() for m in iter]
print

print "global user state"
globaluserstateMessage = r'@badges=staff/1;color=#0D4200;display-name=dallas;emote-sets=0,33,50,237,793,2126,3517,4578,5569,9400,10337,12239;turbo=0;user-id=1337;user-type=admin :tmi.twitch.tv GLOBALUSERSTATE'
iter = TagsCapability.globaluserstate.finditer(globaluserstateMessage)
print [m.groupdict() for m in iter]
print

print "non bits message"
nonBitsMessage = r'@badges=global_mod/1,turbo/1;color=#0D4200;display-name=dallas;emotes=25:0-4,12-16/1902:6-10;id=b34ccfc7-4977-403a-8a94-33c6bac34fb8;mod=0;room-id=1337;subscriber=0;tmi-sent-ts=1507246572675;turbo=1;user-id=1337;user-type=global_mod :ronni!ronni@ronni.tmi.twitch.tv PRIVMSG #dallas :Kappa Keepo Kappa'
iter = TagsCapability.privmsg.finditer(nonBitsMessage)
print [m.groupdict() for m in iter]
print

print "privmsg"
privmsg = r'@badges=moderator/1,subscriber/24;color=#BB1169;display-name=Pig_;emotes=;flags=;id=90c971eb-3534-43c4-bc54-723d6d369c62;mod=1;room-id=23964412;subscriber=1;tmi-sent-ts=1537669071344;turbo=0;user-id=41932978;user-type=mod :pig_!pig_@pig_.tmi.twitch.tv PRIVMSG #fullgrowngaming :Hockey was at 2 today, not 6 like is usually is'
iter = TagsCapability.privmsg.finditer(privmsg)
print [m.groupdict() for m in iter]
print

print "bits message"
bitsMessage = r'@badges=staff/1,bits/1000;bits=100;color=;display-name=dallas;emotes=;id=b34ccfc7-4977-403a-8a94-33c6bac34fb8;mod=0;room-id=1337;subscriber=0;tmi-sent-ts=1507246572675;turbo=1;user-id=1337;user-type=staff :ronni!ronni@ronni.tmi.twitch.tv PRIVMSG #dallas :cheer100'
iter = TagsCapability.privmsg.finditer(bitsMessage)
print [m.groupdict() for m in iter]
print

print "user join message"
userjoinMessage = r'@broadcaster-lang=en;r9k=0;slow=0;subs-only=0 :tmi.twitch.tv ROOMSTATE #dallas'
iter = TagsCapability.roomstate.finditer(userjoinMessage)
print [m.groupdict() for m in iter]
print

print "slow mode message"
slowmodeMessage = r'@slow=10 :tmi.twitch.tv ROOMSTATE #dallas'
iter = TagsCapability.roomstate.finditer(slowmodeMessage)
print [m.groupdict() for m in iter]
print

print "resub message"
resubMessage = r'@badges=staff/1,broadcaster/1,turbo/1;color=#008000;display-name=ronni;emotes=;id=db25007f-7a18-43eb-9379-80131e44d633;login=ronni;mod=0;msg-id=resub;msg-param-months=6;msg-param-sub-plan=Prime;msg-param-sub-plan-name=Prime;room-id=1337;subscriber=1;system-msg=ronni\shas\ssubscribed\sfor\s6\smonths!;tmi-sent-ts=1507246572675;turbo=1;user-id=1337;user-type=staff :tmi.twitch.tv USERNOTICE #dallas :Great stream -- keep it up!'
iter = TagsCapability.subnotice.finditer(resubMessage)
print [m.groupdict() for m in iter]
print

print "gift sub message"
giftsubMessage = r'@badges=staff/1,premium/1;color=#0000FF;display-name=TWW2;emotes=;id=e9176cd8-5e22-4684-ad40-ce53c2561c5e;login=tww2;mod=0;msg-id=subgift;msg-param-months=1;msg-param-recipient-display-name=Mr_Woodchuck;msg-param-recipient-id=89614178;msg-param-recipient-name=mr_woodchuck;msg-param-sub-plan-name=House\sof\sNyoro~n;msg-param-sub-plan=1000;room-id=19571752;subscriber=0;system-msg=TWW2\sgifted\sa\sTier\s1\ssub\sto\sMr_Woodchuck!;tmi-sent-ts=1521159445153;turbo=0;user-id=13405587;user-type=staff :tmi.twitch.tv USERNOTICE #forstycup'
iter = TagsCapability.giftnotice.finditer(giftsubMessage)
print [m.groupdict() for m in iter]
print

print "raid message"
raidMessage = r'@badges=turbo/1;color=#9ACD32;display-name=TestChannel;emotes=;id=3d830f12-795c-447d-af3c-ea05e40fbddb;login=testchannel;mod=0;msg-id=raid;msg-param-displayName=TestChannel;msg-param-login=testchannel;msg-param-viewerCount=15;room-id=56379257;subscriber=0;system-msg=15\sraiders\sfrom\sTestChannel\shave\sjoined\n!;tmi-sent-ts=1507246572675;turbo=1;user-id=123456;user-type= :tmi.twitch.tv USERNOTICE #othertestchannel'
iter = TagsCapability.raidnotice.finditer(raidMessage)
print [m.groupdict() for m in iter]
print

print "ritual message"
ritualMessage = r'@badges=;color=;display-name=SevenTest1;emotes=30259:0-6;id=37feed0f-b9c7-4c3a-b475-21c6c6d21c3d;login=seventest1;mod=0;msg-id=ritual;msg-param-ritual-name=new_chatter;room-id=6316121;subscriber=0;system-msg=Seventoes\sis\snew\shere!;tmi-sent-ts=1508363903826;turbo=0;user-id=131260580;user-type= :tmi.twitch.tv USERNOTICE #seventoes :HeyGuys'
iter = TagsCapability.ritualnotice.finditer(ritualMessage)
print [m.groupdict() for m in iter]
print

print "user joins channel message"
userstate = r'@badges=staff/1;color=#0D4200;display-name=ronni;emote-sets=0,33,50,237,793,2126,3517,4578,5569,9400,10337,12239;mod=1;subscriber=1;turbo=1;user-type=staff :tmi.twitch.tv USERSTATE #dallas'
iter = TagsCapability.userstate.finditer(userstate)
print [m.groupdict() for m in iter]
print