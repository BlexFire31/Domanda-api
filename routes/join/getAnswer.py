from utils.db import database
from flask import Blueprint, request, copy_current_request_context
from utils.functions import runAsyncTask, isInt
from utils.web_tokens import validateJWT

api = Blueprint("getAnswer", __name__)


@api.route("/get", methods=["POST", ])
def getCorrectAnswer():
    isValidJWT, userData = validateJWT(request.form.get("token"))
    if (
        isInt(request.form.get("code")) and
        isValidJWT and
        isInt(request.form.get("question"))
    ):  # Checking whether required params are correct

        quizRef = database.collection(request.form.get("code").strip())

        ####################-------------MULTI THREADING VERIFICATIONS-------------####################

        verifications = {
            "isFinished": None,
            "hasAttempted": None,
            "correctAnswer": None,
        }

        @copy_current_request_context
        def hasAttempted(state=[]):

            state.append(
                quizRef
                .document("Questions")
                .collection(request.form.get("question").strip())
                .document("Answers")
                .collection("Answers")
                .document(userData.get("name"))
                .get().exists
            )
            verifications.update({
                "hasAttempted":
                # error if does not exists
                (False, "You need to attempt the question first") if state[0] != True
                else (True, "")
            })
        runAsyncTask(
            hasAttempted
        )  # name is in Members collection

        @copy_current_request_context
        def isFinished(state=[]):

            state.append(
                quizRef
                .document("Questions")
                .collection(request.form.get("question").strip())
                .document("QuestionData")
                .get()
            )
            if state[0].exists == False:
                verifications.update({
                    "isFinished":
                    (False, "This Quiz/Question does not exist")
                })
            elif state[0].to_dict().get("finished") != True:
                verifications.update({
                    "isFinished":
                    (False, "You cannot get the correct answer now ;P ")
                })
            else:
                verifications.update({
                    "isFinished":
                    (True, "")
                })
        runAsyncTask(
            isFinished
        )  # question has finished

        @copy_current_request_context
        def getCorrectAnswer(state=[]):

            state.append(
                quizRef
                .document("Questions")
                .collection(request.form.get("question").strip())
                .document("CorrectAnswer")
                .get()
            )
            verifications.update({
                "correctAnswer":
                (False, "This Quiz/Question does not exist") if state[0].exists == False
                else (True, state[0].to_dict().get("option"))
            })
        runAsyncTask(
            getCorrectAnswer
        )  # get the correct answer

        # wait till threads have completed, while waiting check for any failed cases, if failed cases are found, alert user immediately
        while None in list(verifications.values()):
            values = verifications.values()
            for case in values:
                if case == None:
                    continue
                if case[0] == False:
                    return {"success": False, "error": case[1]}

        for case in verifications.values():
            if case[0] == False:
                return {"success": False, "error": case[1]}

        return {"success": True, "data": verifications.get("correctAnswer")[1]}

    else:
        return {"success": False, "error": "Parameters passed are incorrect"}
