import os
import sys
import getopt
from Twitch.AuthenticatedUser import AuthenticatedUser
from BotInterfaces.BotInstance import BotInstance
from Twitch.TwitchConnection import TwitchConnection
from Twitch.TestConnection import TestConnection
from ComponentLoader import ComponentLoader


def main(argv):
    bot = BotInstance()
    tokenFile = os.path.join(os.path.dirname(__file__),
                                     "TwitchToken.json")

    settings_dir = os.path.join(os.path.dirname(__file__), "Settings")
    components = ComponentLoader.get_components(settings_dir)

    for component in components:
        bot.add_component(component)

    botuser = AuthenticatedUser(tokenFile)
    connection = TwitchConnection(botuser, argv[0])
    bot.set_connection(connection)
    bot.start()

    PAUSE = True

    message = raw_input('> ')

    while message != 'q':
        bot.send_message(message)
        message = raw_input('> ')
        print(str(message))

    bot.stop()
    return


if __name__ == "__main__":
    main(sys.argv[1:])
