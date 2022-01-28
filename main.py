from flask import Flask
from routes import app as routes
from secrets import token_hex
import os
from dotenv import load_dotenv

app = Flask(
    __name__,
)

app.register_blueprint(
    routes
)
load_dotenv()  # Load .env file from local system (for development)
app.secret_key = token_hex()
app.config["WEB_CONFIG"] = os.environ["WEB_CONFIG"]

@app.after_request
def on_request(response):
    response.headers["Access-Control-Allow-Origin"]="*";
    return response