import time
from threading import Timer
import random

from Commands.Trigger import *
from Commands.Response import *


class RockPaperScissorsAddon(object):
    def __init__(self, adaptor):
        if not isinstance(adaptor, RockPaperScissorsAdaptor):
            raise TypeError('adaptor must be RockPaperScissorsAdaptor')

        self.adaptor = adaptor
        self.Games = {}

        def timeout(sender):
            self.adaptor.timeout()
            del self.Games[sender.user]
            return

        def response(msg):
            self.adaptor.response(msg)
            return

        def gameover(sender, result):
            self.adaptor.gameover(result)
            del self.Games[sender.user]
            return

        def startRPS(sender, msg, *args):
            if msg.Sender in self.Games:
                return

            rps = RockPaperScissors(msg.Sender)
            rps.onTimeout = timeout
            rps.onResponse = response
            rps.onGameOver = gameover

            self.Games[msg.Sender] = rps

            rps.Start()
            self.adaptor.started()
            return

        def playRPS(sender, msg, *args):
            if msg.Sender not in self.Games:
                self.adaptor.unexpected_command(msg)
                return

            move = msg.Message[1:]
            self.Games[msg.Sender].Play(move)
            return

        rps1 = adaptor.generate_start_trigger('!rockpaperscissors')
        rps2 = adaptor.generate_start_trigger('!rps')

        rpsR = adaptor.generate_trigger('!rock')
        rpsP = adaptor.generate_trigger('!paper')
        rpsS = adaptor.generate_trigger('!scissors')

        rpsResp = CodeResponse(5, startRPS)
        rpsPlayResp = CodeResponse(5, playRPS)

        rpsResp.addTrigger(rps1)
        rpsResp.addTrigger(rps2)
        rpsPlayResp.addTrigger(rpsR)
        rpsPlayResp.addTrigger(rpsP)
        rpsPlayResp.addTrigger(rpsS)


class RockPaperScissorsAdaptor(object):
    def generate_start_trigger(self, text):
        return

    def generate_trigger(self, text):
        return

    def started(self):
        return

    def timeout(self):
        return

    def response(self, msg):
        return

    def gameover(self, result):
        return

    def unexpected_command(self, msg):
        return


class RockPaperScissors(object):
    tie = 0
    loss = 1
    win = 2

    rock = "rock"
    paper = "paper"
    scissors = "scissors"

    options = {
        0: rock,
        1: paper,
        2: scissors
    }

    def __init__(self, user):
        self.user = user
        self.onResponse = None
        self.onTimeout = None
        self.onGameOver = None

        #timer
        self.Timeout = None
        return

    def Start(self):
        def timeout():
            if self.onTimeout is not None:
                self.onTimeout(self)

        self.Timeout = Timer(10, timeout)
        self.Timeout.start()
        return

    def Play(self, playerMove):
        if not self.Timeout.is_alive():
            return

        self.Timeout.cancel()
        playerMove = playerMove.lower()

        if playerMove != RockPaperScissors.rock and \
                playerMove != RockPaperScissors.paper and \
                playerMove != RockPaperScissors.scissors:
            return

        value = random.randint(0, 2)
        botMove = RockPaperScissors.options.get(value)
        self.onResponse(botMove)

        if playerMove == botMove:
            result = RockPaperScissors.tie
        elif (playerMove == RockPaperScissors.rock and botMove ==
              RockPaperScissors.paper) or \
             (playerMove == RockPaperScissors.paper and botMove ==
              RockPaperScissors.scissors) or \
             (playerMove == RockPaperScissors.scissors and botMove ==
              RockPaperScissors.rock):
            result = RockPaperScissors.win
        else:
            result = RockPaperScissors.loss

        time.sleep(1.2)

        self.onGameOver(self, result)
        return
