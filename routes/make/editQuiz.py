from utils.functions import deleteResponses, isInt, verify_id_token
from routes.make.makeQuiz import setQuizInFirebase
from routes.make.validateAndPrepareQuizData import validateAndPrepareQuizData
from utils.db import database
from flask import Blueprint, request
from utils.functions import runAsyncTask


api = Blueprint("editQuiz", __name__)


@api.route("/edit", methods=["POST"])
def edit():
    user = verify_id_token(request.form.get("token"))
    if user == None:  # checks whether user is signed in

        return {
            "inProgress": False,
            "error": "You are not signed in"
        }

    if not isInt(request.form.get("code")):
        return {
            "inProgress": False,
            "error": "Code passed is invalid"
        }
    # Checks if quiz exists and is owner
    quiz = database.collection(request.form.get(
        "code").strip()).document("Host").get()
    if not quiz.exists:
        return {
            "inProgress": False,
            "error": "This quiz does not exist"
        }
    elif quiz.get("Host") != user["uid"]:
        return {
            "inProgress": False,
            "error": "You are not the owner of this quiz"
        }

    success, data = validateAndPrepareQuizData(request.form.get("data"))

    if(success):
        code = int(request.form.get("code"))

        database.collection(str(code)).document("Questions").update(
            {"activeQuestion": "-2"})  # Set active question to 0 before updating data
        # Delete the questions that are not there in the new data
        quizLength = database.collection(request.form.get("code").strip()).document(
            "Questions").get().get("questionsLength")
        newQuizLength = len(data)

        for q in range(1, newQuizLength+1):
            runAsyncTask(deleteResponses, database
                         .collection(request.form.get("code").strip())
                         .document("Questions")
                         .collection(str(q)),
                         False  # do not delete parent document ("Answers")
                         )
        if newQuizLength < quizLength:  # Delete extra questions
            for q in range(newQuizLength+1, quizLength+1):
                runAsyncTask(database
                             .collection(request.form.get("code").strip())
                             .document("Questions")
                             .collection(str(q))
                             .document("QuestionData")
                             .delete,)
                runAsyncTask(database
                             .collection(request.form.get("code").strip())
                             .document("Questions")
                             .collection(str(q))
                             .document("CorrectAnswer")
                             .delete,)
                runAsyncTask(deleteResponses, database
                             .collection(request.form.get("code").strip())
                             .document("Questions")
                             .collection(str(q)),
                             True  # delete parent document ("Answers")
                             )

        runAsyncTask(setQuizInFirebase, data, user["uid"], code, True)

        return {
            "inProgress": True,
            "code": code
        }
    else:
        return {
            "inProgress": False,
            "error": "The Data passed is invalid"
        }
