import time
from threading import Timer
import random
from Trigger import *
from Response import *
from BotComponent import BotComponent


class RockPaperScissorsAddon(object):
    Games = {}

    def __init__(self, component, adaptor):
        if not isinstance(component, BotComponent):
            raise TypeError('component must be BotComponent')

        if not isinstance(adaptor, RockPaperScissorsAdaptor):
            raise TypeError('adaptor must be RockPaperScissorsAdaptor')

        self.adaptor = adaptor

        def timeout():
            self.adaptor.timeout()
            return

        def response(msg):
            self.adaptor.response(msg)
            return

        def gameover(sender, result):
            self.adaptor.gameover(result)
            del RockPaperScissorsAddon.Games[sender.user]
            return

        def startRPS(msg, *args):
            if msg.Sender in RockPaperScissorsAddon.Games:
                return

            rps = RockPaperScissors(msg.Sender)
            rps.onTimeout = timeout
            rps.onResponse = response
            rps.onGameOver = gameover

            RockPaperScissorsAddon.Games[msg.Sender] = rps

            rps.Start()
            adaptor.started()
            return

        def playRPS(msg, *args):

            if msg.Sender not in RockPaperScissorsAddon.Games:
                self.adaptor.unexpected_command(msg)
                return

            move = msg.Message[1:]
            RockPaperScissorsAddon.Games[msg.Sender].Play(move)
            return

        rps1 = Trigger('!rockpaperscissors')
        rps2 = Trigger('!rps')
        rpsResp = CodeResponse(5, startRPS)
        rpsResp.addTrigger(rps1)
        rpsResp.addTrigger(rps2)

        rpsR = Trigger('!rock')
        rpsP = Trigger('!paper')
        rpsS = Trigger('!scissors')
        rpsPlayResp = CodeResponse(5, playRPS)
        rpsPlayResp.addTrigger(rpsR)
        rpsPlayResp.addTrigger(rpsP)
        rpsPlayResp.addTrigger(rpsS)

        component.triggers.append(rps1)
        component.triggers.append(rps2)
        component.triggers.append(rpsR)
        component.triggers.append(rpsP)
        component.triggers.append(rpsS)


class RockPaperScissorsAdaptor(object):
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
        self.Timeout = None
        return

    def Start(self):
        def timeout():
            if self.onTimeout is not None:
                self.onTimeout()

        self.Timeout = Timer(10, timeout)
        self.Timeout.start()
        return

    def Play(self, playerMove):
        if not self.Timeout.is_alive():
            self.onResponse("We're not playing, silly")
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

        time.sleep(1)

        self.onGameOver(self, result)
        return
