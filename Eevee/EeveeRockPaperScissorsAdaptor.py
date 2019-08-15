from BotComponents.RockPaperScissors import RockPaperScissorsAdaptor, RockPaperScissors


class RockPaperScissorsEeveeAdaptor(RockPaperScissorsAdaptor):
    def __init__(self, eevee):
        super(RockPaperScissorsEeveeAdaptor, self).__init__()
        self.eevee = eevee
        return

    def generate_start_trigger(self, text):
        trigger = self.eevee.adaptor.trigger_factory.create_trigger(text)
        self.eevee.happiness.game_triggers.append(trigger)
        return trigger

    def generate_trigger(self, text):
        trigger = self.eevee.adaptor.trigger_factory.create_trigger(text)
        return trigger

    def started(self):
        self.eevee.adaptor.send_message("LETS PLAY! GO!")
        return

    def timeout(self):
        self.eevee.adaptor.send_message("Awww you said you'd play with me")
        self.eevee.happiness.Update(-5)
        return

    def response(self, msg):
        s = msg + "!!!!!!"
        self.eevee.adaptor.send_message(s)
        return

    def gameover(self, win):
        if win == RockPaperScissors.loss:
            self.eevee.adaptor.send_message("You big meanie YesYou")
            self.eevee.happiness.Update(-5)
        elif win == RockPaperScissors.win:
            self.eevee.adaptor.send_message("Yay I WIN!!!!")
            self.eevee.happiness.Update(80)
        else:
            self.eevee.adaptor.send_message("Awww... Play again?")
            self.eevee.happiness.Update(50)
        return

    def unexpected_command(self, msg):
        self.eevee.adaptor.send_message(
            "@" + msg.Sender + " we're not playing silly!")
        self.eevee.happiness.Update(10)
        return


