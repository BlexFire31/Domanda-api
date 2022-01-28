from utils.db import database
from flask import Blueprint, request
from utils.functions import runAsyncTask, isInt

api = Blueprint("getStatus", __name__)


@api.route("/getStatus", methods=["POST"])
def getStatus():
    # Returns the data of all questions

    if isInt(request.form.get("code")):
        quizRef = database.collection(request.form.get(
            "code").strip()).document("Questions").get()

        if (
            quizRef.exists
        ):
            questionsLength = quizRef.to_dict().get("questionsLength")
            answers = {}

            # gets the 'started' and 'finished' params of a question and adds it to questions dictionary
            def hasQuestionStartedFinished(questionRef):

                questionData = questionRef.document(
                    "QuestionData").get().to_dict()
                answers[questionRef.id] = {
                    "started": questionData.get("started"),
                    "finished": questionData.get("finished"),
                    "title": questionData.get("title"),
                    "optionA": questionData.get("optionA"),
                    "optionB": questionData.get("optionB"),
                    "optionC": questionData.get("optionC"),
                    "optionD": questionData.get("optionD"),
                    "optionE": questionData.get("optionE"),
                    "optionF": questionData.get("optionF"),
                }

            for question in range(1, questionsLength+1):
                runAsyncTask(
                    hasQuestionStartedFinished,
                    database
                    .collection(request.form.get("code").strip())
                    .document("Questions")
                    .collection(str(question))
                )  # to do multi threading and make it happen faster

            while len(answers) != questionsLength:
                pass  # waiting till all the threads have finished their task

            return {"success": True, "data": answers}
        else:
            return {"success": False, "error": "This quiz doesn't exist"}
    else:
        return {"success": False, "error": "Parameters passed are incorrect"}
