from EeveeResponse import EeveeResponse
from RockPaperScissors import *
from BotComponent import BotComponent


class Eevee(BotComponent):
    MIN_HAPPINESS = 0
    MAX_HAPPINESS = 600

    HappinessTick = 60

    def __init__(self, connection):
        super(Eevee, self).__init__(connection)

        self.Happiness = 300
        self.t = None

        def HappyTick():
            self.ChangeHappiness(-1)
            self.t = Timer(Eevee.HappinessTick, HappyTick)
            self.t.start()
            return

        eeveeTrigger = Trigger('!play')
        eeveeResponse = EeveeResponse(self, self.connection)
        eeveeResponse.addTrigger(eeveeTrigger)
        self.triggers.append(eeveeTrigger)

        HappyTick()
        return

    def shutdown(self):
        self.t.cancel()
        return

    def MessageReceived(self, msg):
        for trigger in self.triggers:
            trigger.invoke(msg)
        return

    def ChangeHappiness(self, value):
        self.Happiness += value
        return


class RockPaperScissorsEeveeAdaptor(RockPaperScissorsAdaptor):
    def __init__(self, eevee):
        super(RockPaperScissorsEeveeAdaptor, self).__init__()
        self.eevee = eevee
        return

    def started(self):
        self.eevee.connection.send_message("LETS PLAY! GO!")
        return

    def timeout(self):
        self.eevee.connection.send_message("Awww you said you'd play with me")
        self.eevee.ChangeHappiness(-5)
        return

    def response(self, msg):
        s = msg + "!!!!!!"
        self.eevee.connection.send_message(s)
        return

    def gameover(self, win):
        if win == RockPaperScissors.loss:
            self.eevee.connection.send_message("You big meanie YesYou")
            self.eevee.ChangeHappiness(-5)
        elif win == RockPaperScissors.win:
            self.eevee.connection.send_message("Yay I WIN!!!!")
            self.eevee.ChangeHappiness(30)
        else:
            self.eevee.connection.send_message("Awww... Play again?")
            self.eevee.ChangeHappiness(15)
        return

    def unexpected_command(self, msg):
        self.eevee.connection.send_message(
            "@" + msg.Sender + " we're not playing silly!")
        return
