from flask import jsonify
from apps.flask_app import app
from apps.socket_app import ws
from apps.mongo_client import client
from time import sleep


@ws.route("/<int:arg>")
def handler(ws, arg):
    print(type(arg))
    while True:
        ws.send(arg)
        sleep(50)


app.run(port=8000, host="0.0.0.0")
