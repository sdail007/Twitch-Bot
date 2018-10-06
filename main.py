import os
import sys
import getopt
from threading import Event
from Twitch.AuthenticatedUser import AuthenticatedUser
from Commands.BotInstance import BotInstance
from Twitch.TwitchConnection import TwitchConnection
from Twitch.TestConnection import TestConnection

from Streamlabs.StreamLabsConnection import StreamLabsConnection


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "c:f:")
    except getopt.GetoptError:
        print 'main.py -c <channel> | -f <file>'
        sys.exit(2)

    connection = None

    sltoken = os.path.join(os.path.dirname(__file__), "StreamLabsToken.json")
    # slconnection = StreamLabsConnection(sltoken)

    for opt, arg in opts:
        if opt == '-c':
            tokenFile = os.path.join(os.path.dirname(__file__), "Token.json")
            botuser = AuthenticatedUser(tokenFile)
            connection = TwitchConnection(botuser, arg)
        elif opt == '-f':
            connection = TestConnection(arg)

    settings_dir = os.path.join(os.path.dirname(__file__), "Settings")
    bot = BotInstance(connection, settings_dir)

    bot.start()

    message = raw_input('> ')

    while message != 'q':
        bot.send_message(message)
        message = raw_input('> ')
        print str(message)

    bot.shutdown()
    return


if __name__ == "__main__":
    main(sys.argv[1:])
