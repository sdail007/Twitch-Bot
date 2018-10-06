from Web.websocket_server import WebsocketServer
import threading
import codecs
import json


class Event(object):
    @classmethod
    def fromSettings(cls, settings):
        return cls(settings['text'])

    def __init__(self, text):
        self.text = text
        return

    def dumpAsDict(self):
        return {"text": self.text}


class EventList(object):
    def __init__(self, cls=Event, eventsFile=None):
        self.ConnectionHandler = WebsocketServer(1000, host='127.0.0.1')

        self.file = eventsFile

        if self.file is not None:
            with codecs.open(self.file, encoding="utf-8-sig", mode="r") as f:
                settings = json.load(f, encoding="utf-8")

            self.recentEvents = [cls.fromSettings(recentEvent)
                                 for recentEvent in settings['RecentEvents']]
        else:
            self.recentEvents = []

        self.ConnectionHandler.set_fn_new_client(self.NewClient)

        serverThread = threading.Thread(target=self.ConnectionHandler.run_forever)
        serverThread.daemon = True
        serverThread.start()

    def NewClient(self, client, server):
        for recentEvent in self.recentEvents[-3:]:
            self.ConnectionHandler.send_message(client, json.dumps(recentEvent.dumpAsDict()))
        return

    def add_event(self, event):
        self.recentEvents.append(event)
        self.ConnectionHandler.send_message_to_all(json.dumps(event.dumpAsDict()))
        self.Save()

    def dumpAsDict(self):
        recentEvents = []
        for recentEvent in self.recentEvents:
            recentEvents.append(recentEvent.dumpAsDict())
        return {"RecentEvents": recentEvents}

    def Save(self):
        with codecs.open(self.file, encoding="utf-8-sig", mode="w+") as f:
            json.dump(self.dumpAsDict(), f, encoding="utf-8", indent=2,
                      sort_keys=True)
        return

    def __del__(self):
        self.ConnectionHandler.shutdown()
        return

