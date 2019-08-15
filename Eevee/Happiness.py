from Commands.Response import CodeResponse
from HealthBase import HealthBase


class Happiness(HealthBase):
    def __init__(self, eevee, settings=None):
        super(Happiness, self).__init__(settings)
        self.eevee = eevee

        cuddleResponse = CodeResponse(15, self.cuddle)
        eeveeResponse = CodeResponse(5, self.printPlayCommands)

        cuddleTrigger = eevee.adaptor.trigger_factory.create_trigger("!cuddle")
        eeveeTrigger = eevee.adaptor.trigger_factory.create_trigger("!play")

        cuddleResponse.addTrigger(cuddleTrigger)
        eeveeResponse.addTrigger(eeveeTrigger)

    def printPlayCommands(self, sender, msg, *args):
        cmds = ", ".join(map(str, self.game_triggers))
        output = "I can play games! " + cmds
        self.eevee.adaptor.send_message(output)
        return

    def cuddle(self, sender, msg, *args):
        self.eevee.adaptor.send_message("YAAAAAAAAAAAAAAAAAAY SNUGS <3")
        self.Update(30)
        return

