import websocket
import thread

from ChatMessage import ChatMessage
from AuthenticatedUser import AuthenticatedUser
from ChatInterface import ChatInterface


class TwitchConnection(ChatInterface):
    ping = 'PING :tmi.twitch.tv'

    def __init__(self, user, channel):
        if not isinstance(user, AuthenticatedUser):
            raise TypeError('user must be set to an AuthenticatedUser')
        super(TwitchConnection, self).__init__()
        self.user = user
        self.channel = channel.lower()

        #message received from channel
        def on_message(ws, message):
            message = message.rstrip('\r\n')

            print message

            #pong when pinged (IRC compliance)
            if message == TwitchConnection.ping:
                def pong(*args):
                    self.ws.send('PONG :tmi.twitch.tv')

                thread.start_new_thread(pong, ())
                return

            #Decode message and propogate to listeners
            chat_message = ChatMessage(message)
            self.MessageReceived.invoke(self, chat_message)

        #connection successful
        def on_open(ws):
            def run(*args):
                #authenticate and join channel (IRC compliance)
                self.ws.send('PASS ' + self.user.token)
                self.ws.send('NICK ' + self.user.nick)
                self.ws.send('JOIN #' + self.channel)

                #get extra info with messages like subs and bits (Twitch custom)
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

        #setup connection to Twitch
        self.ws = websocket.WebSocketApp('wss://irc-ws.chat.twitch.tv:443',
                                         on_message=on_message,
                                         on_close=on_close,
                                         on_error=on_error,
                                         on_open=on_open)
        return

    #Open connection
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


