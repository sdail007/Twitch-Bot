import thread
import os
from AuthenticatedUser import AuthenticatedUser
from TwitchConnection import TwitchConnection


global connection

if __name__ == "__main__":

    tokenFile = os.path.join(os.path.dirname(__file__), "Token.json")
    botuser = AuthenticatedUser(tokenFile)

    connection = TwitchConnection(botuser, 'truelove429')

    def startBot():
        global connection
        connection.start()
    thread.start_new_thread(startBot, ())

    message = raw_input('Do a barrel roll: ')

    while message != 'q':
        connection.send_message(message)
        message = raw_input('Do a barrel roll: ')
        print str(message)