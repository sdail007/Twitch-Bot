import websocket
import thread
from ChatMessage import ChatMessage
from AuthenticatedUser import AuthenticatedUser
from InvocationList import InvocationList


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
                self.ws.send('PONG :tmi.twitch.tv')
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
        self.ws.run_forever()

    def send_message(self, message):
        def run(*args):
            self.ws.send('PRIVMSG #' + self.channel + ' :' + message)

        thread.start_new_thread(run, ())

    def __del__(self):
        self.ws.send('PART #' + self.channel)
        self.ws.close()