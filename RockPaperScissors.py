import time
from threading import Timer
import random
from Trigger import *
from Response import *
from BotComponent import BotComponent


class RockPaperScissorsGame(object):
    Games = {}

    @classmethod
    def Initialize(cls, component):
        if not isinstance(component, BotComponent):
            raise TypeError('component must be BotComponent')

        def startRPS(msg, *args):
            if msg.Sender in RockPaperScissorsGame.Games:
                return

            game = RockPaperScissorsGame(msg.Sender, component)
            RockPaperScissorsGame.Games[msg.Sender] = game
            component.connection.send_message("LETS PLAY! GO!")
            game.rps.Start()
            return

        def playRPS(msg, *args):
            if msg.Sender not in RockPaperScissorsGame.Games:
                component.connection.send_message("@" + msg.Sender + " we're not "
                                                                 "playing "
                                                                 "silly!")
                return

            move = msg.Message[1:]
            RockPaperScissorsGame.Games[msg.Sender].rps.Play(move)
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

    def __init__(self, user, eevee):
        self.user = user

        def timeout():
            eevee.connection.send_message("Awww you said you'd play with me")
            eevee.ChangeHappiness(-5)
            return

        def response(msg):
            s = msg + "!!!!!!"
            eevee.connection.send_message(s)
            return

        def gameover(win):
            if win == RockPaperScissors.loss:
                eevee.connection.send_message("You big meanie YesYou")
                eevee.ChangeHappiness(-5)
            elif win == RockPaperScissors.win:
                eevee.connection.send_message("Yay I WIN!!!!")
                eevee.ChangeHappiness(30)
            else:
                eevee.connection.send_message("Awww... Play again?")
                eevee.ChangeHappiness(15)
            del RockPaperScissorsGame.Games[self.user]
            return

        self.rps = RockPaperScissors()
        self.rps.onTimeout = timeout
        self.rps.onResponse = response
        self.rps.onGameOver = gameover
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

    def __init__(self):
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

        self.onGameOver(result)
        return
