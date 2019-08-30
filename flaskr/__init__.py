import os
from Twitch.AuthenticatedUser import AuthenticatedUser
from BotInterfaces.BotInstance import BotInstance
from Twitch.TwitchConnection import TwitchConnection
from ComponentLoader import ComponentLoader

from flask import Flask, request, escape


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',   #change to random value when deploying
        DATABASE=os.path.join(app.instance_path, 'flask.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    tokenFile = os.path.join(app.instance_path, "TwitchToken.json")
    botuser = AuthenticatedUser(tokenFile)
    connection = TwitchConnection(botuser, 'truelove429')

    bot = BotInstance()

    settings_dir = os.path.join(app.instance_path, "Settings")
    components = ComponentLoader.get_components(settings_dir)

    bot.start(connection)

    for component in components:
        bot.add_component(component)

    @app.route('/send')
    def hello():
        message = request.args.get("msg", "Hello World")
        bot.send_message(message)
        return 'Sent: {0}!'.format(escape(message))

    @app.route('/stop', methods=['POST'])
    def stop():
        if request.method == 'POST':
            print request.form
            operation = request.form.get('operation', 'missing')
            if operation.lower() == 'stop':
                bot.shutdown()
                return 'success'
            elif operation.lower() == 'start':
                bot.start(connection)
                return 'success'
        return 'you cray cray'

    return app

