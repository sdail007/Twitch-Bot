import thread
import os
from AuthenticatedUser import AuthenticatedUser
from TwitchConnection import TwitchConnection
from Trigger import Trigger
from ChatMessage import ChatMessage
from Response import Response
from Cooldown import Cooldown

import Readers

global connection


if __name__ == "__main__":
    tokenFile = os.path.join(os.path.dirname(__file__), "Token.json")
    botuser = AuthenticatedUser(tokenFile)

    connection = TwitchConnection(botuser, 'fullgrowngaming')

    def MessageReceived(msg):
        print(msg)
        for key, value in triggers.Triggers.items():
            value.invoke(msg)

    dir = os.path.dirname(__file__)
    triggers = Readers.Triggers(dir)
    cooldowns = Readers.Cooldowns(dir)
    responses = Readers.Responses(dir, connection, cooldowns)
    links = Readers.Links(dir)

    for key, value in links.__dict__.items():
        r = responses.Responses[value["Response"]]
        t = triggers.Triggers[value["Trigger"]]
        r.addTrigger(t)
        print "linking: ", t, " to ", r

    connection.MessageReceived.add(MessageReceived)

    def startBot():
        global connection
        connection.start()
    thread.start_new_thread(startBot, ())

    message = raw_input('Do a barrel roll: ')

    while message != 'q':
        connection.send_message(message)
        message = raw_input('Do a barrel roll: ')
        print str(message)
