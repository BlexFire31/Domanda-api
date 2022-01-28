from utils.db import database
from flask import Blueprint, request, copy_current_request_context
from utils.functions import runAsyncTask, isInt, verify_id_token

api = Blueprint("hostAll", __name__)


@api.route("/all", methods=["POST"])
def hostAll():

    if(
        isInt(request.form.get("code")) and
        request.form.get("method") in ("START", "FINISH")
    ):  # Checks for Required Parameters

        quizRef = database.collection(request.form.get("code").strip())

        ####################-------------MULTI THREADING VERIFICATIONS-------------####################

        verifications = {
            "activeQuestion": None,
            "host": None
        }

        @copy_current_request_context
        def isOwner(state=[]):

            state.append(
                quizRef
                .document("Host")
                .get()
            )
            if (state[0].exists == False):
                verifications.update({"host": (False, "Quiz does not exist")})
            else:
                user = verify_id_token(request.form.get("token"))
                if(user != None and state[0].to_dict().get("Host") == user["uid"]):
                    verifications.update({"host": (True, "")})
                else:
                    verifications.update(
                        {"host": (False, "You are not the owner of this quiz")})

        runAsyncTask(
            isOwner
        )  # is the owner of quiz and checks if quiz exists

        @copy_current_request_context
        def getActiveQuestion(state=[]):

            state.append(
                quizRef
                .document("Questions")
                .get()
            )
            if (state[0].exists == False):
                verifications.update(
                    {"activeQuestion": (False, "Quiz does not exist")})
            else:
                verifications.update(
                    {"activeQuestion": (True, state[0].to_dict())})

        runAsyncTask(
            getActiveQuestion
        )  # get activeQuestion & questionsLength data
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

        questionsLength = int(verifications.get(
            "activeQuestion")[1].get("questionsLength"))

        if(request.form.get("method") == "START"):
            for question in range(1, questionsLength+1):
                runAsyncTask(
                    quizRef
                    .document("Questions")
                    .collection(str(question))
                    .document("QuestionData")
                    .update,
                    {"finished": False, "started": True}
                )

            runAsyncTask(
                quizRef
                .document("Questions")
                .update,
                # -1 integer means all questions are started
                {"activeQuestion": -1}
            )

        elif(request.form.get("method") == "FINISH"):
            for question in range(1, questionsLength+1):
                runAsyncTask(
                    quizRef
                    .document("Questions")
                    .collection(str(question))
                    .document("QuestionData")
                    .update,
                    {"finished": True, "started": True}
                )

            runAsyncTask(
                quizRef
                .document("Questions")
                .update,
                # 0 string means all questions are started
                {"activeQuestion": "0"}
            )

        return {"success": True, }

    return {"success": False, "error": "Parameters passed are incorrect"}
