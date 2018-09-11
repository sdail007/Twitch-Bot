from Trigger import Trigger
from Response import CodeResponse
from HealthBase import HealthBase


class Hunger(HealthBase):
    def __init__(self, connection, settings=None):
        super(Hunger, self).__init__(connection, settings)

        def treat(sender, msg, *args):
            self.Update(50)
            self.connection.send_message("om nom nom nom")
            return

        def printEatCommands(sender, msg, *args):
            cmds = ", ".join(map(str, self.triggers))
            output = "I can eat things! " + cmds
            self.connection.send_message(output)
            return

        eeveeTrigger = Trigger('!eat')
        eeveeResponse = CodeResponse(5, printEatCommands)
        eeveeResponse.addTrigger(eeveeTrigger)
        self.triggers.append(eeveeTrigger)

        eeveeTrigger = Trigger('!treat')
        eeveeResponse = CodeResponse(5, treat)
        eeveeResponse.addTrigger(eeveeTrigger)
        self.triggers.append(eeveeTrigger)
