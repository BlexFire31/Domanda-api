from routes.make.validateAndPrepareQuizData import validateAndPrepareQuizData
from routes.make.makeQuiz import setQuizInFirebase
from utils.db import database
from flask import Blueprint, request
from utils.functions import runAsyncTask, verify_id_token


api = Blueprint("createQuiz", __name__)


@api.route("/create", methods=["POST"])
def create():
    user = verify_id_token(request.form.get("token"))
    if user == None:  # checks whether user is signed in

        return {
            "inProgress": False,
            "error": "You are not signed in"
        }

    success, data = validateAndPrepareQuizData(request.form.get("data"))

    if(success):
        code = database.collection("DATA").document(
            "quiz-code").get().to_dict().get("number")+1
        # we update the count incase a new question is created by another client | The client knows when their question has been created when questionLength gets a value
        database.collection("DATA").document(
            "quiz-code").update({"number": code})
        runAsyncTask(setQuizInFirebase, data, user["uid"], code)

        return {
            "inProgress": True,
            "code": code
        }
    else:
        return {
            "inProgress": False,
            "error": "The data passed is invalid"
        }
