from utils.db import database
from flask import Blueprint, request, copy_current_request_context
from utils.functions import runAsyncTask, isInt, verify_id_token

api = Blueprint("hostSingle", __name__)


@api.route("/single", methods=["POST"])
def hostSingle():

    if (
        isInt(request.form.get("code")) and
        request.form.get("method") in ("START", "FINISH")
    ):  # Checks for Required Parameters

        if (
            request.form.get("method") == "START"
            and not isInt(request.form.get("question"))
        ):  # if method is start and question is not provided, throw error
            return {"success": False, "error": "Invalid Question"}

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

        if request.form.get("method") == "START":

            if int(request.form.get("question").strip()) not in range(1, questionsLength+1):
                return {"success": False, "error": "This question doesn't exist"}

            for question in range(1, questionsLength+1):
                isFinished = str(question) != request.form.get(
                    "question").strip()
                runAsyncTask(
                    quizRef
                    .document("Questions")
                    .collection(str(question))
                    .document("QuestionData")
                    .update,
                    {
                        "finished": isFinished,  # Start the question user requested, finish the others
                    }
                )
            runAsyncTask(
                quizRef
                .document("Questions")
                .update,
                {
                    # we don't have to worry about exception handling here because it already checks whether that doc exists, and all docs are numbers
                    # if the type is integer, that means it is active, if it is string, it is inactive
                    "activeQuestion": int(request.form.get("question").strip())
                }
            )

        elif request.form.get("method") == "FINISH":
            activeQuestion = int(verifications.get(
                "activeQuestion")[1].get("activeQuestion"))

            runAsyncTask(
                quizRef
                .document("Questions")
                # Only 1 question can be active at a time, otherwise all questions should be active
                .collection(str(activeQuestion))
                .document("QuestionData")
                .update,
                {"finished": True, }
            )

            runAsyncTask(
                database
                .collection(request.form.get("code").strip())
                .document("Questions")
                .update,
                {
                    # if the type is integer, that means it is active, if it is string, it is inactive
                    "activeQuestion": str(activeQuestion)
                }
            )

        return {"success": True, }

    else:
        return {"success": False, "error": "Parameters passed are incorrect"}
