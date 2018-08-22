#Embedded file name: C:\Users\Stephen\PycharmProjects\TwitchPlaysTicTacToe\AuthenticatedUser.py
import codecs
import json

class AuthenticatedUser(object):

    def __init__(self, nick, token):
        self.nick = nick
        self.token = token

    def __init__(self, f):
        with codecs.open(f, encoding='utf-8-sig', mode='r') as f:
            parts = json.load(f, encoding='utf-8')
            self.nick = parts['nick']
            self.token = parts['token']
