from flask import Blueprint
from routes.host.finish import api as finishApi
from routes.host.startAll import api as startAllApi
from routes.host.startSingle import api as hostSingleApi

app = Blueprint("ApiHost", __name__)
app.register_blueprint(finishApi)
app.register_blueprint(startAllApi)
app.register_blueprint(hostSingleApi)
