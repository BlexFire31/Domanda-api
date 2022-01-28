from flask import Blueprint
from routes.host.getStatus import api as getStatusApi
from routes.host.hostAll import api as hostAllApi
from routes.host.hostSingle import api as hostSingleApi

app = Blueprint("ApiHost", __name__)
app.register_blueprint(getStatusApi)
app.register_blueprint(hostAllApi)
app.register_blueprint(hostSingleApi)
