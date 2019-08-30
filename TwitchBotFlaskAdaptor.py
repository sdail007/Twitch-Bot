from Twitch.AuthenticatedUser import AuthenticatedUser
from BotInterfaces.BotInstance import BotInstance
from Twitch.TwitchConnection import TwitchConnection
from Twitch.TestConnection import TestConnection
from ComponentLoader import ComponentLoader
import flask

import os


def Create_Context():
    tokenFile = os.path.join(os.path.dirname(__file__), "TwitchToken.json")
    botuser = AuthenticatedUser(tokenFile)
    connection = TwitchConnection(botuser, 'truelove429')

    bot = BotInstance()

    settings_dir = os.path.join(os.path.dirname(__file__), "Settings")
    components = ComponentLoader.get_components(settings_dir)

    bot.start(connection)

    for component in components:
        bot.add_component(component)

    return bot

