import os
import sys
import getopt
from AuthenticatedUser import AuthenticatedUser
from BotInstance import BotInstance


def main(argv):
    if len(argv) != 1:
        sys.stderr.write('Twitch channel required')
        sys.exit(1)

    channel = argv[0]

    tokenFile = os.path.join(os.path.dirname(__file__), "Token.json")
    botuser = AuthenticatedUser(tokenFile)
    dir = os.path.join(os.path.dirname(__file__), "Settings")

    bot = BotInstance(botuser, channel, dir)

    message = raw_input('Do a barrel roll: ')

    while message != 'q':
        bot.send_message(message)
        message = raw_input('Do a barrel roll: ')
        print str(message)


if __name__ == "__main__":
    main(sys.argv[1:])
