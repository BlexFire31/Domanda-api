from flask import Blueprint
from routes.make import app as makeApp
from routes.host import app as hostApp
from routes.join import app as joinApp

app = Blueprint("RouteApi", __name__)
app.register_blueprint(makeApp, url_prefix="/make")
app.register_blueprint(hostApp, url_prefix="/host")
app.register_blueprint(joinApp, url_prefix="/join")
