from threading import Thread
from re import findall as regex_findall
from google.cloud.firestore import CollectionReference
from google.cloud.firestore_v1.document import DocumentReference
from utils.db import auth


def runAsyncTask(target, *args):
    Thread(target=target, args=args).start()


def validateName(name: str) -> tuple[bool, str]:
    if (name == None or name.strip() == ""):
        return False, "Name cannot be empty"

    if(len(regex_findall(r"__((\s)?(\S)?)*__", name.strip())) != 0):
        return False, "Name cannot be surrounded by 2 underscores (_)"
    if(
        "".join(
            regex_findall("([a-zA-Z1-9]|\s|_|-)", name.strip())
        ) != name.strip()
    ):
        return False, "Name can only contain alphabets, numbers and symbols(_,-)"
    return True, ""


def isInt(code):
    try:
        int(code)
        return True
    except:
        return False


def isNotEmptyString(string: str):
    try:
        v = string.strip()
        if v == "":
            return False
    except:
        return False
    return True


def deleteResponses(collection: CollectionReference, parent: bool = True):
    answers: DocumentReference = collection.document("Answers")
    collectionDocuments: list[DocumentReference] = [
        (doc.reference) for doc in answers.collection("Answers").get()]
    for document in collectionDocuments:
        runAsyncTask(document.delete)
    if(parent):
        runAsyncTask(answers.delete)


def verify_id_token(token: str) -> dict:
    try:
        return auth.verify_id_token(token)
    except:
        return None
