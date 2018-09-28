from Commands.BotComponent import BotComponent
from Commands.Trigger import Trigger
from Commands.Response import *
from Commands.Cooldown import Cooldown
from threading import Timer


class Outfit(object):
    @classmethod
    def FromSettings(cls, settings):
        color = settings["Color"]
        points = settings["Points"]
        return Outfit(color, points)

    def __init__(self, color, points):
        self.color = color
        self.points = points
        self.likedBerry = None
        self.dislikedBerry = None
        return

    def dump_as_dict(self):
        '''
        :return:
        '''
        return {"Color": self.color,
                "Points": self.points}


class Wardrobe(object):
    def __init__(self, settings):
        self.Outfits = {}
        for key in settings:
            self.Outfits[key] = Outfit.FromSettings(settings[key])
        return

    def GetFavoriteOutfit(self):
        favorite = max(self.Outfits.iterkeys(), key=lambda k: self.Outfits[
            k].points)
        return favorite

    def dump_as_dict(self):
        '''
        :return:
        '''

        output = {}
        for t in self.Outfits:
            output[t] = self.Outfits[t].dump_as_dict()
        return output


class DressUp(BotComponent):
    def __init__(self, connection, happiness, settings):
        super(DressUp, self).__init__(connection)

        self.happiness = happiness
        self.outfitKey = settings["Outfit"]
        self.Wardrobe = Wardrobe(settings["Wardrobe"])
        self.outfit = self.Wardrobe.Outfits[self.outfitKey]
        self.PointsTimer = Timer(10, self.IncrementPoints)

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
            self.outfit = self.Wardrobe.Outfits[self.outfitKey]

            self.PointsTimer.cancel()
            self.PointsTimer = Timer(10, self.IncrementPoints)
            self.PointsTimer.start()

            self.happiness.Update(50)

            sender.send_message("/color {}".format(self.outfit.color))
            sleep(0.5)
            sender.send_message("/me MWEEE I'm {}!".format(newForm))
            return

        def PrintFave(sender, msg, *args):
            favorite = self.Wardrobe.GetFavoriteOutfit()
            sender.send_message("My favorite outfit is {}!".format(favorite))
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

        triggerKeys = [t.Text for t in self.triggers]
        outfitst = Trigger("!outfits")
        message = 'Try one of these to change my outfit! ' + ', '.join(
            triggerKeys)
        outfitsr = Response(message)
        outfitsr.addTrigger(outfitst)
        self.triggers.append(outfitst)

        favoritet = Trigger("!favorite")
        favoriter = CodeResponse(10, PrintFave)
        favoriter.addTrigger(favoritet)
        self.triggers.append(favoritet)

        self.PointsTimer.start()
        return

    def IncrementPoints(self):
        self.outfit.points += 1

        self.PointsTimer = Timer(10, self.IncrementPoints)
        self.PointsTimer.start()
        return

    def shutdown(self):
        self.PointsTimer.cancel()
        return

    def dump_as_dict(self):
        '''
        :return:
        '''
        return {"Outfit": self.outfitKey,
                "Wardrobe": self.Wardrobe.dump_as_dict()}

