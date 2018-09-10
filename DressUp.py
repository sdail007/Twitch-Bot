from BotComponent import BotComponent
from Trigger import Trigger
from Response import *
from Cooldown import Cooldown


class Outfit(object):
    def __init__(self, color):
        self.color = color
        self.likedBerry = None
        self.dislikedBerry = None
        return


class Wardrobe(object):
    Outfits = {
        "Flareon": Outfit("Coral"),
        "Vaporeon": Outfit("Blue"),
        "Jolteon": Outfit("YellowGreen"),
        "Espeon": Outfit("BlueViolet"),
        "Umbreon": Outfit("GoldenRod"),
        "Glaceon": Outfit("DodgerBlue"),
        "Leafeon": Outfit("Green"),
        "Sylveon": Outfit("HotPink")
    }


class DressUp(BotComponent):
    def __init__(self, connection, happiness,
                 settings=Wardrobe.Outfits["Flareon"]):
        super(DressUp, self).__init__(connection)

        self.happiness = happiness
        self.outfitKey = settings["Outfit"]
        self.outfit = Wardrobe.Outfits[self.outfitKey]

        stone = Cooldown(10)

        flareon = Trigger("!fire")
        vaporeon = Trigger("!water")
        jolteon = Trigger("!thunder")
        espeon = Trigger("!sunlight")
        umbreon = Trigger("!moonlight")
        glaceon = Trigger("!ice")
        leafeon = Trigger("!moss")
        sylveon = Trigger("!amie")

        def ChangeForms(sender, msg, *args):
            newForm = args[0][0]
            self.outfitKey = newForm
            self.outfit = Wardrobe.Outfits[self.outfitKey]

            self.happiness.Update(50)

            sender.send_message("/color {}".format(self.outfit.color))
            sleep(0.5)
            sender.send_message("/me MWEEE I'm {}!".format(newForm))
            return

        flareonr = CodeResponse(stone, ChangeForms, "Flareon")
        vaporeonr = CodeResponse(stone, ChangeForms, "Vaporeon")
        jolteonr = CodeResponse(stone, ChangeForms, "Jolteon")
        espeonr = CodeResponse(stone, ChangeForms, "Espeon")
        umbreonr = CodeResponse(stone, ChangeForms, "Umbreon")
        glaceonr = CodeResponse(stone, ChangeForms, "Glaceon")
        leafeonr = CodeResponse(stone, ChangeForms, "Leafeon")
        sylveonr = CodeResponse(stone, ChangeForms, "Sylveon")

        flareonr.addTrigger(flareon)
        vaporeonr.addTrigger(vaporeon)
        jolteonr.addTrigger(jolteon)
        espeonr.addTrigger(espeon)
        umbreonr.addTrigger(umbreon)
        glaceonr.addTrigger(glaceon)
        leafeonr.addTrigger(leafeon)
        sylveonr.addTrigger(sylveon)

        self.triggers.append(flareon)
        self.triggers.append(vaporeon)
        self.triggers.append(jolteon)
        self.triggers.append(espeon)
        self.triggers.append(umbreon)
        self.triggers.append(glaceon)
        self.triggers.append(leafeon)
        self.triggers.append(sylveon)
        return

    def dump_as_dict(self):
        '''
        :return:
        '''
        return {"Outfit": self.outfitKey}
