from typing import Literal
from utils.functions import isNotEmptyString

allOptionsType = Literal[
    "optionA",
    "optionB",
    "optionC",
    "optionD",
    "optionE",
    "optionF"]
allOptionsList = [
    "optionA",
    "optionB",
    "optionC",
    "optionD",
    "optionE",
    "optionF"]


class Question:
    def __init__(
        self,
        id: int,
        correctOption: allOptionsType,
        title: str,
        options: dict[allOptionsType, str]
    ):
        self.id = id
        self.correctOption = correctOption
        self.title = title
        self.options = options

    def validate(self) -> bool:
        # ---Tests made---
        # Each parameter is not None
        # id is integer
        # optionA and optionB is not None
        # title, non-None options shouldn't be empty (string but no content)
        # correctOption is Valid
        # correctOption in options is not None
        # id is greater than 0

        if(
            self.id == None or
            self.title == None or
            self.options == None or
            self.correctOption == None
        ):  # Parameter's shouldn't be None
            return False

        if(
            self.options.get("optionA") == None or
            self.options.get("optionB") == None
        ):  # optionA and optionB shouldn't be null
            return False

        if(
            not isNotEmptyString(self.title)
        ):  # title shouldn't be empty
            return False

        # options that are not None shouldn't be empty
        if(False in [isNotEmptyString(str(option)) for option in self.options.values()]):
            return False

        if(
            self.correctOption not in allOptionsList
        ):  # correctOption should be valid
            return False

        if(
            self.options.get(self.correctOption) == None
        ):  # correctOption in options shouldn't be None
            return False

        try:
            intId = int(self.id)
        except:  # id should be an integer
            return False

        if(
            intId <= 0
        ):  # id should be greater than 0
            return False

        return True

    def toDict(self) -> dict:
        return {
            "optionA": self.options.get("optionA"),
            "optionB": self.options.get("optionB"),
            "optionC": self.options.get("optionC"),
            "optionD": self.options.get("optionD"),
            "optionE": self.options.get("optionE"),
            "optionF": self.options.get("optionF"),
            "correctOption": self.correctOption,
            "title": self.title,
            "id": self.id,
        }
