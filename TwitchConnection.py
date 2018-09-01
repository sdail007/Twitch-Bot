import websocket
import thread
from time import sleep

from ChatMessage import ChatMessage
from AuthenticatedUser import AuthenticatedUser
from InvocationList import InvocationList
from Response import ResponseBase


class TwitchConnection(object):
    ping = 'PING :tmi.twitch.tv'

    def __init__(self, user, channel):
        if not isinstance(user, AuthenticatedUser):
            raise TypeError('user must be set to an AuthenticatedUser')
        self.user = user
        self.channel = channel.lower()
        self.MessageReceived = InvocationList()

        def on_message(ws, message):
            message = message.rstrip('\r\n')

            if message == TwitchConnection.ping:
                def pong(*args):
                    self.ws.send('PONG :tmi.twitch.tv')

                thread.start_new_thread(pong, ())
                return

            chat_message = ChatMessage(message)
            self.MessageReceived.invoke(chat_message)

        def on_open(ws):
            def run(*args):
                self.ws.send('PASS ' + self.user.token)
                self.ws.send('NICK ' + self.user.nick)
                self.ws.send('JOIN #' + self.channel)
                self.ws.send('CAP REQ :twitch.tv/tags')
                self.ws.send('CAP REQ :twitch.tv/membership')
                self.ws.send('CAP REQ :twitch.tv/commands')

                print "Connected to ", self.channel
            thread.start_new_thread(run, ())

        def on_error(ws, error):
            print 'error'
            print error

        def on_close(ws):
            print 'Closed'

        self.ws = websocket.WebSocketApp('wss://irc-ws.chat.twitch.tv:443',
                                         on_message=on_message,
                                         on_close=on_close,
                                         on_error=on_error,
                                         on_open=on_open)

    def start(self):
        def run(*args):
            self.ws.run_forever()
        thread.start_new_thread(run, ())

    def send_message(self, message):
        def send(*args):
            self.ws.send('PRIVMSG #' + self.channel + ' :' + message)
            print self.user.nick + ": " + message
        thread.start_new_thread(send, ())

    def __del__(self):
        self.ws.send('PART #' + self.channel)
        self.ws.close()


class Response(ResponseBase):
    def __init__(self, connection, string, cooldown=10):
        super(Response, self).__init__(cooldown)
        self.connection = connection
        self.string = string

    def respond(self, message):
        print message.Message
        if self.cooldown.Consume():
            for m in self.string.split('\n'):
                self.connection.send_message(m)
                sleep(0.5)

    def __str__(self):
        return self.string + " " + str(self.cooldown)
