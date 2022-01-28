import os
from jwt import encode, decode
from calendar import timegm as toEpoch
from datetime import datetime


def validateJWT(token) -> tuple[bool, dict]:
    secret_key = os.environ["ADMIN_CONFIG"]
    algorithm = ["HS256", ]
    current_date = toEpoch(datetime.now().timetuple())

    # check if jwt is valid/can be serialized

    try:
        data = decode(token, key=secret_key, algorithms=algorithm)
    except:  # jwt was probably modified/tampered with
        return False, {}

    # check if jwt has expired

    if data.get("exp") < current_date:
        return False, {}

    return True, data


def createJWT(uid, name):
    payload = {
        "name": name,
        "sub": str(uid),
        "iat": toEpoch(datetime.now().timetuple()),
        # one hour in seconds
        "exp": toEpoch(datetime.now().timetuple())+3600,
    }
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    secret_key = os.environ["ADMIN_CONFIG"]

    token = encode(payload=payload, headers=headers,
                   algorithm="HS256", key=secret_key)
    return token
