import os
import sys
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

    message = raw_input('> ')

    while message != 'q':
        bot.send_message(message)
        message = raw_input('> ')
        print str(message)

    bot.shutdown()


if __name__ == "__main__":
    main(sys.argv[1:])
