from threading import Timer
from BotComponent import BotComponent
from Trigger import Trigger
from Response import CodeResponse


class Hunger(BotComponent):
    MIN_HUNGER = 0
    MAX_HUNGER = 600

    Tick = 36

    def __init__(self, connection, eevee_settings):
        super(Hunger, self).__init__(connection)
        self.settings = eevee_settings
        self.commands = []

        def HungerTick():
            self.Update(-1)

            self.hungerTimer = Timer(Hunger.Tick, HungerTick)
            self.hungerTimer.start()
            return

        def treat(sender, msg, *args):
            self.Update(50)
            self.connection.send_message("om nom nom nom")
            return

        eeveeTrigger = Trigger('!treat')
        eeveeResponse = CodeResponse(5, treat)
        eeveeResponse.addTrigger(eeveeTrigger)
        self.triggers.append(eeveeTrigger)

        self.hungerTimer = Timer(Hunger.Tick, HungerTick)
        self.hungerTimer.start()

    def Clamp(self, value):
        return min(max(Hunger.MIN_HUNGER, value), Hunger.MAX_HUNGER)

    def Update(self, value):
        newHunger = self.settings.Hunger + value
        self.settings.Hunger = self.Clamp(newHunger)
        self.settings.save()
