from BotComponents.PokeBlockGame import PokeBlockGameAdaptor


class EeveePokeBlockGameAdaptor(PokeBlockGameAdaptor):

    responses = [
        "AWW That's no fun!",
        "I'm still hungry",
        "mmmMMMmmmm",
        "Tasty!",
        "THICCCCC"
    ]

    def __init__(self, eevee):
        super(EeveePokeBlockGameAdaptor, self).__init__()
        self.eevee = eevee
        return

    def register(self, addon):
        self.eevee.happiness.triggers.extend(addon.triggers)
        self.eevee.hunger.triggers.extend(addon.triggers)
        return

    def started(self):
        self.eevee.connection.send_message("I LOVE POKEBLOCKS")
        return

    def gameover(self, result):
        count = min(len(EeveePokeBlockGameAdaptor.responses) - 1, len(result))
        reward = count * 25
        self.eevee.happiness.Update(reward)
        self.eevee.hunger.Update(reward)

        response = EeveePokeBlockGameAdaptor.responses[count]
        self.eevee.connection.send_message(response)
        return

    def unexpected_command(self, msg):
        return
