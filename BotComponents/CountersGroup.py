import os
import codecs
import json

from Commands.BotComponent import BotComponent
from Commands.Counter import Counter
from Commands.Trigger import Trigger
from Commands.Response import CodeResponse


class CountersGroup(BotComponent):
    def __init__(self, file, connection):
        super(CountersGroup, self).__init__(connection)
        self.file = file
        pathparts = os.path.split(file)[-1]
        self.groupname = pathparts[:-5]

        self.counters = {}

        with codecs.open(self.file, encoding="utf-8-sig", mode="r") as f:
            fileCounters = json.load(f, encoding="utf-8")
            for counterName in fileCounters:
                counter = Counter.fromSettings(counterName, fileCounters[
                    counterName])
                self.counters[counterName] = counter

        for ctr in self.counters:
            self.createCounterTriggers(self.counters[ctr])

        t = Trigger("!" + self.groupname)
        r = CodeResponse(10, self.AddCounter)
        r.addTrigger(t)
        self.triggers.append(t)
        return

    def dump_as_dict(self):
        dict = {}
        for t in self.counters:
            dict[t] = self.counters[t].dumpAsDict()
        return dict

    def shutdown(self):
        with codecs.open(self.file, encoding="utf-8-sig", mode="w+") as f:
            json.dump(self.dump_as_dict(), f, encoding="utf-8", indent=4,
                      sort_keys=True)
        return

    def increment(self, sender, message, *arg):
        ctr = arg[0][0]
        ctr.Increment()
        sender.send_message(ctr.getResponse())
        return

    def createCounterTriggers(self, ctr):
        t = Trigger("!" + ctr.name)
        r = CodeResponse(10, self.increment, ctr)
        r.addTrigger(t)
        self.triggers.append(t)
        return

    def AddCounter(self, sender, message, *args):
        params = message.Message.split(' ')[1:]

        if len(params) == 0:
            sender.send_message('Counters in {}: '.format(self.groupname)
                                + ', '.join(self.counters))
            return

        if params[0].lower() == 'add':
            if len(params) >= 3:
                name = params[1]
                response = ' '.join(params[2:])

                if response.find('{}') == -1:
                    return

                newCounter = Counter(name, response)
                self.createCounterTriggers(newCounter)
                self.counters[name] = newCounter
            return
        elif params[0].lower() == 'del':
            if len(params) != 2:
                return

            name = params[1]
            if name in self.counters:
                del self.counters[name]
        elif params[0].lower() == 'reset':
            if len(params) != 2:
                return

            name = params[1]
            if name in self.counters:
                self.counters[name].Reset()

        return
