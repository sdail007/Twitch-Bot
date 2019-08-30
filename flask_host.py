from flask import Flask, request, escape
import redis
from datetime import datetime
import json

app = Flask(__name__)
redis = redis.Redis()


@app.route('/send')
def send():
    content = request.args.get("msg", "Hello World")
    timestamp = datetime.utcnow().strftime("%Y/%m/%d.%H:%M:%S.%f")

    message = {
        "command": "send_message",
        "timestamp": timestamp,
        "args":
            {
                "content": content
            }
    }
    commandStr = json.dumps(message)

    redis.rpush('messages', commandStr)
    return 'Sent: {0}!'.format(escape(content))


@app.route('/connection')
def connect():
    command = request.args.get("command", None)
    timestamp = datetime.utcnow().strftime("%Y/%m/%d.%H:%M:%S.%f")

    channel = request.args.get("channel", None)

    if command not in ["connect", "disconnect"]:
        return "Invalid Request"

    if command == "connect" and channel is None:
        return "Invalid Request"

    if command == "connect":
        message = {
            "command": "connect",
            "timestamp": timestamp,
            "args":
                {
                    "channel": channel
                }
        }
    elif command == "disconnect":
        message = {
            "command": "disconnect",
            "timestamp": timestamp,
            "args": {}
        }
    else:
        return "Invalid Request"

    commandStr = json.dumps(message)

    redis.rpush('connection', commandStr)

    if command == 'connect':
        return 'Requested connect to: {0}!'.format(escape(channel))
    else:
        return 'Requested disconnect'


@app.route('/stop')
def stop():
    redis.rpush('quit', '')
    return 'bot stopped'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
