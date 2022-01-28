from utils.question import Question
from json import loads as parseJson


def validateAndPrepareQuizData(data) -> tuple[bool, list[Question]]:
    try:
        if data == None or len(data) == 0:
            return False, []
        else:

            try:
                data: list[dict[str, str]] = parseJson(data)
                if not data:
                    return False, []
            except:
                return False, []

            newData: list[Question] = []
            for index, question in enumerate(data):
                newData.append(
                    Question(
                        id=str(index+1),  # enumerate starts at 0
                        correctOption=question.get("correctOption"),
                        title=question.get("title"),
                        options={
                            "optionA": question.get("optionA"),
                            "optionB": question.get("optionB"),
                            "optionC": question.get("optionC"),
                            "optionD": question.get("optionD"),
                            "optionE": question.get("optionE"),
                            "optionF": question.get("optionF"),
                        }
                    )
                )
            for question in newData:
                if(not question.validate()):
                    break
            else:
                # if break statement is not called, it calls else statement after for loop
                return True, newData
            return False, []
    except:
        return False, []
