
from utils.question import Question
from utils.functions import runAsyncTask
from utils.db import database


def setQuizInFirebase(
    data: list[Question],
    uid: str,
    code: int,
    editMode: bool = False
):
    if editMode == False:
        runAsyncTask(
            database
            .collection(str(code))
            .document("Host")
            .set,
            {"Host": uid})  # create host document
        runAsyncTask(
            database
            .collection(str(code))
            .document("Members")
            .set,
            {})
        runAsyncTask(
            database
            .collection(str(code))
            .document("Lobby")
            .set,
            {})
        # setting the questions document to an empty dict so that it doesn't become a virtual document and the client can listen to this document till "questionsLength" is defined
        database.collection(str(code)).document("Questions").set({})

    def createQuestionInFirebase(question: Question):
        firebaseQuestionData = question.toDict()
        firebaseQuestionData.pop("correctOption")
        firebaseQuestionData.pop("id")
        firebaseQuestionData["finished"] = True

        database.collection(str(code)).document("Questions").collection(
            question.id).document("QuestionData").set(firebaseQuestionData)
        runAsyncTask(
            database
            .collection(str(code))
            .document("Questions")
            .collection(question.id)
            .document("CorrectAnswer")
            .set,
            {"option": question.correctOption})
        runAsyncTask(
            database
            .collection(str(code))
            .document("Questions")
            .collection(str(question.id))
            .document("Answers")
            .set,
            {})

    for question in data:
        runAsyncTask(createQuestionInFirebase, question)
    runAsyncTask(
        database
        .collection(str(code))
        .document("Questions")
        .update,
        {"questionsLength": len(data), "activeQuestion": "0" if editMode == False else "-2"})
