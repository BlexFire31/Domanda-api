from apps.flask_app import app
from pymongo.collection import Collection
from models.User import User
from apps.mongo_client import client

@app.post("/new")
@get_user_from_token
def new_quiz(user:User):
    users:Collection[User] = client.data.users

    

    return {"success":True,"code":11} 