from typing import Literal, TypedDict


class User(TypedDict):
    email:str
    provider:Literal['microsoft','google']
    uid:str