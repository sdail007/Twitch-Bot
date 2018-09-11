from Response import CodeResponse
from Trigger import Trigger
from HealthBase import HealthBase


class Happiness(HealthBase):
    def __init__(self, connection, settings=None):
        super(Happiness, self).__init__(connection, settings)

        def printPlayCommands(sender, msg, *args):
            cmds = ", ".join(map(str, self.triggers))
            output = "I can play games! " + cmds
            self.connection.send_message(output)
            return

        eeveeTrigger = Trigger('!play')
        eeveeResponse = CodeResponse(5, printPlayCommands)
        eeveeResponse.addTrigger(eeveeTrigger)
        self.triggers.append(eeveeTrigger)
