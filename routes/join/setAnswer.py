from utils.db import database
from flask import Blueprint, request, copy_current_request_context
from utils.functions import runAsyncTask, isInt
from utils.question import allOptionsList
from utils.web_tokens import validateJWT

api = Blueprint("setAnswer", __name__)


@api.route("/set", methods=["POST"])
def setAnswer():

    isValidJWT, userData = validateJWT(request.form.get("token"))
    if(
        isInt(request.form.get("code")) and
        isValidJWT and
        request.form.get("option") in allOptionsList and
        isInt(request.form.get("question"))
    ):  # Checking whether required params are passed and correct

        quizRef = database.collection(request.form.get("code").strip())

        ####################-------------MULTI THREADING VERIFICATIONS-------------####################

        verifications = {
            "isNotFinished": None,
            "hasJoined": None,
            "hasNotAttempted": None
        }

        @copy_current_request_context
        def hasNotAttempted(state=[]):

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
                "hasNotAttempted":
                # error if exists
                (False, "You have already attempted this question") if state[0] == True
                else (True, "")
            })

        runAsyncTask(
            hasNotAttempted
        )  # name is in Members collection

        @copy_current_request_context
        def isNotFinished(state=[]):

            state.append(
                quizRef
                .document("Questions")
                .collection(request.form.get("question").strip())
                .document("QuestionData")
                .get()
            )
            if not state[0].exists:
                verifications.update({
                    "isNotFinished":
                    (False, "This Quiz/Question does not exist")
                })
            elif state[0].to_dict().get("finished") == True:
                verifications.update({
                    "isNotFinished":
                    (False, "You cannot answer now")
                })
            else:
                verifications.update({
                    "isNotFinished":
                    (True, "")
                })

        runAsyncTask(
            isNotFinished
        )  # question has not finished

        @copy_current_request_context
        def hasJoined(state=[]):

            state.append(
                quizRef
                .document("Members")
                .collection("Members")
                .document(userData.get("name"))
                .get().exists
            )
            verifications.update({
                "hasJoined":
                # error if does not exists
                (False, "You haven't joined the quiz yet") if state[0] == False
                else (True, "")
            })

        runAsyncTask(
            hasJoined
        )  # name is in Members collection

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

        runAsyncTask(
            quizRef
            .document("Questions")
            .collection(request.form.get("question").strip())
            .document("Answers")
            .collection("Answers")
            .document(userData.get("name"))
            .set,
            {"option": request.form.get("option")}
        )

        return {"success": True, }

    else:
        return {"success": False, "error": "Parameters passed are incorrect"}
