from BotComponent import BotComponent
from threading import Timer
from Trigger import Trigger
from Response import *


class PokeBlockGameAddon(object):
    def __init__(self, component, adaptor):
        if not isinstance(component, BotComponent):
            raise TypeError('component must be BotComponent')

        if not isinstance(adaptor, PokeBlockGameAdaptor):
            raise TypeError('adaptor must be PokeBlockGameAdaptor')

        self.triggers = []
        self.component = component
        self.adaptor = adaptor
        self.game = None

        def game_end(berries):
            self.adaptor.gameover(berries)
            return

        def game_start(sender, msg, *args):
            self.game = PokeBlockGame()
            self.game.onGameOver = game_end
            self.game.start()
            self.adaptor.started()
            return

        def play(sender, msg, *args):
            self.game.play(msg.Sender, msg.Params)
            return

        pbcd = Cooldown(60)

        start = Trigger("!BerryBlender")
        start2 = Trigger("!bb")
        startResponse = CodeResponse(pbcd, game_start)
        startResponse.addTrigger(start)
        startResponse.addTrigger(start2)

        spin = Trigger("!spin")
        playResponse = CodeResponse(0, play)
        playResponse.addTrigger(spin)

        berryTrigger = Trigger("!berries")
        berryResponse = Response("My favorite cooking ingredients: " +
                                 ", ".join(PokeBlockGame.berries), 10)
        berryResponse.addTrigger(berryTrigger)

        component.triggers.append(start)
        component.triggers.append(start2)
        component.triggers.append(spin)
        component.triggers.append(berryTrigger)

        self.triggers.append(start)
        self.triggers.append(start2)
        self.adaptor.register(self)
        return


class PokeBlockGameAdaptor(object):
    def register(self, addon):
        return

    def started(self):
        return

    def gameover(self, result):
        return

    def unexpected_command(self, msg):
        return


class PokeBlockGame(object):
    max_berries = 4

    berries = [
        "rawst",
        "cheri",
        "pecha",
        "chesto",
        "aspear",
        "lum",
        "leppa",
        "persim",
        "oran",
        "sitrus",
        "nanab",
        "figy",
        "mago",
        "wiki",
        "lapapa",
        "aguav",
        "pinap",
        "bluk",
        "pamtre",
        "wepear",
        "haban",
        "tanga",
        "kasib",
        "charti",
        "colbur",
        "jaboca",
        "enigma",
        "custap",
        "micle",
        "rowap"
    ]

    def __init__(self):
        self.berries = {}

        self.onGameOver = None

        #Timer
        self.Timeout = None
        return

    def start(self):
        #only start the game once
        if self.Timeout is not None and self.Timeout.is_alive():
            return

        def timeout():
            if self.onGameOver is not None:
                self.onGameOver(self.berries.values())

        self.berries.clear()

        self.Timeout = Timer(20, timeout)
        self.Timeout.start()
        return

    def play(self, sender, berry):
        #game running
        if self.Timeout is None or not self.Timeout.is_alive():
            return

        #one move per person
        if sender in self.berries.keys():
            return

        #only 4 moves total
        if len(self.berries) >= PokeBlockGame.max_berries:
            return

        berry = berry.lower()
        if berry not in PokeBlockGame.berries:
            return

        self.berries[sender] = berry
        return

