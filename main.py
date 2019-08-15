import os
import sys
import getopt
from Twitch.AuthenticatedUser import AuthenticatedUser
from BotInterfaces.BotInstance import BotInstance
from Twitch.TwitchConnection import TwitchConnection
from Twitch.TestConnection import TestConnection
from ComponentLoader import ComponentLoader


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "c:f:")
    except getopt.GetoptError:
        print('main.py -c <channel> | -f <file>')
        sys.exit(2)

    connection = None

    sltoken = os.path.join(os.path.dirname(__file__), "StreamLabsToken.json")
    # slconnection = StreamLabsConnection(sltoken)

    for opt, arg in opts:
        if opt == '-c':
            tokenFile = os.path.join(os.path.dirname(__file__),
                                     "TwitchToken.json")
            botuser = AuthenticatedUser(tokenFile)
            connection = TwitchConnection(botuser, arg)
        elif opt == '-f':
            connection = TestConnection(arg)

    bot = BotInstance(connection)

    settings_dir = os.path.join(os.path.dirname(__file__), "Settings")
    components = ComponentLoader.get_components(settings_dir)

    for component in components:
        bot.add_component(component)

    bot.start()

    message = raw_input('> ')

    while message != 'q':
        bot.send_message(message)
        message = raw_input('> ')
        print(str(message))

    bot.shutdown()
    return


if __name__ == "__main__":
    main(sys.argv[1:])
