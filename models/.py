from typing import List, Dict, Literal

Option = Literal["A", "B", "C", "D", "E", "F"]


class User:
    email: str
    role: List[str]

    def __init__(self, email: str, role: List[str]) -> None:
        self.email = email
        self.role = role


class Config:
    status: List[str]
    active: int
    users: Dict[str, User]

    def __init__(self, status: List[str], active: int, users: Dict[str, User]) -> None:
        self.status = status
        self.active = active
        self.users = users


class Options:
    a: str | None
    b: str | None
    c: str | None
    d: str | None
    e: str | None
    f: str | None

    def __init__(self,
                 a: str | None,
                 b: str | None,
                 c: str | None,
                 d: str | None,
                 e: str | None,
                 f: str | None
                 ) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f


class Question:
    id: int
    title: str
    options: Options
    correct: Option
    answers: Dict[str, Option]

    def __init__(self, id: int, title: str, options: Options, correct: str, answers: Dict[str, Option]) -> None:
        self.id = id
        self.title = title
        self.options = options
        self.correct = correct
        self.answers = answers


class Quiz:
    code: int
    config: Config
    questions: List[Question]

    def __init__(self, code: int, config: Config, questions: List[Question]) -> None:
        self.code = code
        self.config = config
        self.questions = questions
