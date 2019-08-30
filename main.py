import os
import sys
import getopt
import json

from Twitch.AuthenticatedUser import AuthenticatedUser
from BotInterfaces.BotInstance import BotInstance
from Twitch.TwitchConnection import TwitchConnection
from Twitch.TestConnection import TestConnection
from ComponentLoader import ComponentLoader

import redis

r = redis.Redis()

bot = None
botuser = None
componentLoader = None

def Connect(channel):
    connection = TwitchConnection(botuser, channel)
    bot.set_connection(connection)
    bot.start()


def load_components():
    components = componentLoader.activate_all()

    for component in components:
        bot.add_component(component)


def main(argv):
    global botuser, bot, componentLoader

    #Get token from instance directory
    tokenFile = os.path.join(os.path.dirname(__file__), "TwitchToken.json")
    botuser = AuthenticatedUser(tokenFile)

    bot = BotInstance()

    settings_dir = os.path.join(os.path.dirname(__file__), "Settings")
    componentLoader = ComponentLoader(settings_dir)

    load_components()

    PAUSE = True

    while PAUSE:
        kvp = r.blpop(['messages', 'connection', 'quit'], timeout=1)

        if kvp:
            print kvp

            if kvp[0] == 'messages':
                command = json.loads(kvp[1])
                bot.send_message(command["args"]["content"])
            elif kvp[0] == 'connection':
                command = json.loads(kvp[1])
                if command["command"] == 'connect':
                    Connect(command["args"]["channel"])
                elif command["command"] == 'disconnect':
                    bot.stop()
            elif kvp[0] == 'quit':
                PAUSE = False
    bot.stop()
    return


if __name__ == "__main__":
    main(sys.argv[1:])
