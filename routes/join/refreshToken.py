from flask import request, Blueprint

from utils.web_tokens import createJWT, validateJWT


api = Blueprint("refreshToken", __name__)


@api.route("/refreshToken", methods=["POST"])
def refreshToken():
    isValidJWT, userData = validateJWT(request.form.get("token"))

    if(not isValidJWT):
        return {"success": False, "error": "Token is either invalid or has expired"}

    return {"success": True, "token": createJWT(userData.get("uid"), userData.get("name"))}
