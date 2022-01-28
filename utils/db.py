import os
from firebase_admin import initialize_app
from firebase_admin.credentials import Certificate
from firebase_admin.firestore import client
import firebase_admin.auth as auth
from google.cloud.firestore_v1.base_client import BaseClient
from json import loads as parseJson


app = initialize_app(Certificate(parseJson(os.environ["ADMIN_CONFIG"])))
database: BaseClient = client(app=app)
