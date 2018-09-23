import websocket
import thread

from Twitch.ChatMessage import ChatMessage
from AuthenticatedUser import AuthenticatedUser
from Commands.ChatInterface import ChatInterface
from Capabilities.TagsCapability import TagsCapability
from Capabilities.MembershipCapability import MembershipCapability
from Capabilities.CommandsCapability import CommandsCapability

class TwitchConnection(ChatInterface):
    ping = 'PING :tmi.twitch.tv'

    def __init__(self, user, channel):
        if not isinstance(user, AuthenticatedUser):
            raise TypeError('user must be set to an AuthenticatedUser')
        super(TwitchConnection, self).__init__()
        self.user = user
        self.channel = channel.lower()

        self.capabilities = [TagsCapability(),
                             MembershipCapability(),
                             CommandsCapability()]
        #Load translators
        #Translators have CAP REQ to send
        #Translators have Message types they can translate
        #Translators can return translated message of type
        #User must find proper translator
        #Dictionary from message to translator
        #Call translate function to build message
        #Each Message type has invokation list?

        #setup connection to Twitch
        self.ws = websocket.WebSocketApp('wss://irc-ws.chat.twitch.tv:443',
                                         on_message=self.on_message,
                                         on_close=self.on_close,
                                         on_error=self.on_error,
                                         on_open=self.on_open)
        return

    def on_open(self):
        '''
        Handler for web socket opening
        joins channel and subscribes to capabilities
        :return:
        '''
        def run(*args):
            # authenticate and join channel (IRC compliance)
            self.ws.send('PASS ' + self.user.token)
            self.ws.send('NICK ' + self.user.nick)
            self.ws.send('JOIN #' + self.channel)

            # get extra info with messages like subs and bits (Twitch custom)

            for capability in self.capabilities:
                self.ws.send(capability.subscriptionmessage)

            #self.ws.send('CAP REQ :twitch.tv/tags')
            #self.ws.send('CAP REQ :twitch.tv/membership')
            #self.ws.send('CAP REQ :twitch.tv/commands')

            print "Connected to ", self.channel

        thread.start_new_thread(run, ())

    def on_message(self, message):
        '''
        Handler for message received from Twitch
        :param message:
        The text received from the websocket
        :return:
        '''
        message = message.rstrip('\r\n')

        stuff = None
        for capability in self.capabilities:
            stuff = capability.Parse(message)
            if stuff is not None:
                break

        if stuff is None:
            print 'UNABLE TO PARSE {}'.format(message)

        #print message

        # pong when pinged (IRC compliance)
        if message == TwitchConnection.ping:
            def pong(*args):
                self.ws.send('PONG :tmi.twitch.tv')

            thread.start_new_thread(pong, ())
            return

        # Decode message and propogate to listeners
        chat_message = ChatMessage(message)
        self.MessageReceived.invoke(self, chat_message)

    def on_error(self, error):
        '''
        Error handler for websocket
        :param error:
        :return:
        '''
        print 'error'
        print error

    def on_close(self):
        '''
        Handler for closing socket
        :return:
        '''
        print 'Closed'

    def start(self):
        '''
        Start up the Twitch connection
        :return:
        '''
        def run(*args):
            self.ws.run_forever()
        thread.start_new_thread(run, ())

    def stop(self):
        '''
        Stop Twitch Connection
        :return:
        '''
        self.ws.send('PART #' + self.channel)
        self.ws.close()
        return

    def send_message(self, message):
        '''
        Send message to Twitch chat
        :param message:
        :return:
        '''
        def send(*args):
            self.ws.send('PRIVMSG #' + self.channel + ' :' + message)
            print self.user.nick + ": " + message
        thread.start_new_thread(send, ())

    def __del__(self):
        self.stop()


