from utils.db import database
from flask import Blueprint, request, copy_current_request_context
from utils.functions import runAsyncTask, isInt, verify_id_token

api = Blueprint("startAll", __name__)


@api.route("/start-all", methods=["POST"])
def hostAll():

    if(
        isInt(request.form.get("code"))
    ):  # Checks for Required Parameters

        quizRef = database.collection(request.form.get("code").strip())

        hostSnapshot = quizRef.document("Host").get()

        if(hostSnapshot.exists != True):
            return {"success": False, "error": "This quiz does not exist"}
        user = verify_id_token(request.form.get("token"))
        if(user == None or hostSnapshot.to_dict().get("Host") != user.get("uid")):
            return {"success": False, "error": "You are not the owner of this quiz"}

        runAsyncTask(
            quizRef
            .document("Questions")
            .update,
            # -1 int means all questions are started
            {"activeQuestion": -1}
        )

        return {"success": True, }

    return {"success": False, "error": "Parameters passed are incorrect"}
