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

    def generate_start_trigger(self, text):
        trigger = self.eevee.adaptor.trigger_factory.create_trigger(text)
        self.eevee.happiness.game_triggers.append(trigger)
        self.eevee.hunger.game_triggers.append(trigger)
        return trigger

    def generate_trigger(self, text):
        trigger = self.eevee.adaptor.trigger_factory.create_trigger(text)
        return trigger

    def started(self):
        self.eevee.adaptor.send_message("I LOVE POKEBLOCKS")
        return

    def gameover(self, result):
        count = min(len(EeveePokeBlockGameAdaptor.responses) - 1, len(result))
        reward = count * 25
        self.eevee.happiness.Update(reward)
        self.eevee.hunger.Update(reward)

        response = EeveePokeBlockGameAdaptor.responses[count]
        self.eevee.adaptor.send_message(response)
        return

    def unexpected_command(self, msg):
        return
