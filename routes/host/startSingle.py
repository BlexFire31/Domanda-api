from utils.db import database
from flask import Blueprint, request, copy_current_request_context
from utils.functions import runAsyncTask, isInt, verify_id_token

api = Blueprint("startSingle", __name__)


@api.route("/start-single", methods=["POST"])
def hostSingle():

    if (
        isInt(request.form.get("code")) and
        isInt(request.form.get("question"))
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
            try:
                values = list(verifications.values())
                for case in values:
                    if case == None:
                        continue
                    if case[0] == False:
                        return {"success": False, "error": case[1]}
            except:  # dictionary size changed during iteration
                continue
        for case in verifications.values():
            if case[0] == False:
                return {"success": False, "error": case[1]}

        questionsLength = int(verifications.get(
            "activeQuestion")[1].get("questionsLength"))

        # This question does not exist
        if int(request.form.get("question")) not in range(1, questionsLength+1):
            return {"success": False, "error": "This question does not exist"}

        runAsyncTask(
            database
            .collection(request.form.get("code").strip())
            .document("Questions")
            .update,
            {
                # if the type is integer, that means it is active, if it is string, it is inactive
                "activeQuestion": int(request.form.get("question"))
            }
        )

        return {"success": True, }

    else:
        return {"success": False, "error": "Parameters passed are incorrect"}
