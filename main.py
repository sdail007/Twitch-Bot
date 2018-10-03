import os
import sys
import getopt
from threading import Event
from Twitch.AuthenticatedUser import AuthenticatedUser
from Commands.BotInstance import BotInstance
from Twitch.TwitchConnection import TwitchConnection


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "c:f:")
    except getopt.GetoptError:
        print 'main.py -c <channel> | -f <file>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-c':
            channel(arg)
        elif opt == '-f':
            file(arg)
    return


def file(file):
    print file

    tokenFile = os.path.join(os.path.dirname(__file__), "Token.json")
    botuser = AuthenticatedUser(tokenFile)
    connection = TwitchConnection(botuser, botuser.nick)

    settings_dir = os.path.join(os.path.dirname(__file__), "Settings")
    bot = BotInstance(connection, settings_dir)

    Event().wait(10)

    # Inject messages into bot ^_^b
    with open(file) as w:
        lines = w.readlines()
    for line in lines:
        connection.on_message(line)

    bot.shutdown()
    return


def channel(channel):
    print 'channel'

    tokenFile = os.path.join(os.path.dirname(__file__), "Token.json")
    botuser = AuthenticatedUser(tokenFile)
    connection = TwitchConnection(botuser, channel)

    settings_dir = os.path.join(os.path.dirname(__file__), "Settings")
    bot = BotInstance(connection, settings_dir)

    connection.start()

    message = raw_input('> ')

    while message != 'q':
        bot.send_message(message)
        message = raw_input('> ')
        print str(message)

    bot.shutdown()
    return


if __name__ == "__main__":
    main(sys.argv[1:])
