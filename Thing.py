import thread
import os
from AuthenticatedUser import AuthenticatedUser
from TwitchConnection import TwitchConnection
from Trigger import Trigger
from ChatMessage import ChatMessage
from Response import Response
from Cooldown import Cooldown

global connection

def MessageReceived(msg):
    print(msg)
    for trigger in Trigger.Triggers:
        trigger.invoke(msg)


if __name__ == "__main__":
    tokenFile = os.path.join(os.path.dirname(__file__), "Token.json")
    botuser = AuthenticatedUser(tokenFile)

    connection = TwitchConnection(botuser, 'truelove429')

    ChatMessage.MessageReceived.add(MessageReceived)

    eevee = Trigger("!eevee")
    r1 = Response(connection, "Hi I'm Eevee", 0)
    r1.addTrigger(eevee)

    vulpix = Trigger("!vulpix")
    r2 = Response(connection, "Hi I'm Vulpix", 0)
    r2.addTrigger(vulpix)

    stone = Cooldown(10)

    vaporeon = Trigger("!water")
    flareon = Trigger("!fire")
    jolteon = Trigger("!thunder")

    rv = Response(connection, "/color Blue\n/me MWEEE I'm Vaporeon!", stone)
    rf = Response(connection, "/color FireBrick\n/me MWEEE I'm Flareon!",
                  stone)
    rj = Response(connection, "/color GoldenRod\n/me MWEEE I'm Jolteon!",
                  stone)

    rv.addTrigger(vaporeon)
    rf.addTrigger(flareon)
    rj.addTrigger(jolteon)

    def startBot():
        global connection
        connection.start()
    thread.start_new_thread(startBot, ())

    message = raw_input('Do a barrel roll: ')

    while message != 'q':
        connection.send_message(message)
        message = raw_input('Do a barrel roll: ')
        print str(message)