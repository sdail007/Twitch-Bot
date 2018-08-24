import os
from AuthenticatedUser import AuthenticatedUser
from BotInstance import  BotInstance

if __name__ == "__main__":
    tokenFile = os.path.join(os.path.dirname(__file__), "Token.json")
    botuser = AuthenticatedUser(tokenFile)
    dir = os.path.join(os.path.dirname(__file__), "Settings")

    bot = BotInstance(botuser, "fullgrowngaming", dir)

    message = raw_input('Do a barrel roll: ')

    while message != 'q':
        bot.send_message(message)
        message = raw_input('Do a barrel roll: ')
        print str(message)
