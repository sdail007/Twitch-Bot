from Commands.Response import CodeResponse
from HealthBase import HealthBase


class Hunger(HealthBase):
    def __init__(self, eevee, settings=None):
        super(Hunger, self).__init__(settings)
        self.eevee = eevee

        eatR = CodeResponse(5, self.printEatCommands)
        treatR = CodeResponse(5, self.treat)

        eatT = eevee.adaptor.trigger_factory.create_trigger("!eat")
        treatT = eevee.adaptor.trigger_factory.create_trigger("!treat")

        eatR.addTrigger(eatT)
        treatR.addTrigger(treatT)

    def treat(self, sender, msg, *args):
        self.Update(50)
        self.eevee.adaptor.send_message("om nom nom nom")
        return

    def printEatCommands(self, sender, msg, *args):
        cmds = ", ".join(map(str, self.game_triggers))
        output = "I can eat things! " + cmds
        self.eevee.adaptor.send_message(output)
        return
