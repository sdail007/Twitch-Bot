from Commands.Trigger import Trigger
from Commands.Response import CodeResponse
from HealthBase import HealthBase


class Hunger(HealthBase):
    def __init__(self, connection, settings=None):
        super(Hunger, self).__init__(connection, settings)
        eeveeTrigger = Trigger('!eat')
        eeveeResponse = CodeResponse(5, self.printEatCommands)
        eeveeResponse.addTrigger(eeveeTrigger)
        self.triggers.append(eeveeTrigger)

        eeveeTrigger = Trigger('!treat')
        eeveeResponse = CodeResponse(5, self.treat)
        eeveeResponse.addTrigger(eeveeTrigger)
        self.triggers.append(eeveeTrigger)

    def treat(self, sender, msg, *args):
        self.Update(50)
        self.connection.send_message("om nom nom nom")
        return

    def printEatCommands(self, sender, msg, *args):
        cmds = ", ".join(map(str, self.game_triggers))
        output = "I can eat things! " + cmds
        self.connection.send_message(output)
        return
