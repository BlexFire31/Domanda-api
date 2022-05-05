from flask_sock import Sock
from apps.flask_app import app

ws = Sock(app)
