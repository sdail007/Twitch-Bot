from Commands.Response import CodeResponse
from Commands.Trigger import Trigger
from HealthBase import HealthBase


class Happiness(HealthBase):
    def __init__(self, connection, settings=None):
        super(Happiness, self).__init__(connection, settings)

        cuddleTrigger = Trigger("!cuddle")
        cuddleResponse = CodeResponse(15, self.cuddle)
        cuddleResponse.addTrigger(cuddleTrigger)
        self.triggers.append(cuddleTrigger)

        eeveeTrigger = Trigger('!play')
        eeveeResponse = CodeResponse(5, self.printPlayCommands)
        eeveeResponse.addTrigger(eeveeTrigger)
        self.triggers.append(eeveeTrigger)

    def printPlayCommands(self, sender, msg, *args):
        cmds = ", ".join(map(str, self.game_triggers))
        output = "I can play games! " + cmds
        self.connection.send_message(output)
        return

    def cuddle(self, sender, msg, *args):
        self.connection.send_message("YAAAAAAAAAAAAAAAAAAY SNUGS <3")
        self.Update(30)
        return

