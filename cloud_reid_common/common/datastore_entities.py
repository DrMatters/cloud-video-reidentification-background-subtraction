from typing import Any, Union

from pydantic import BaseModel


class Comment(BaseModel):
    post_id: int
    text: str
    owner_id: int
    post_owner_id: int
    id: int
    known_class: Union[int, None]
    date: int
    predicted_probability: Union[float, None]
    thread: Any
    from_id: int
    group_id: int
    parents_stack: Any


class Group(BaseModel):
    id: int
    confirmation_key: str
    model_kind: str
    model_path: str
    preprocessor_kind: str
    secret: str


class User(BaseModel):
    username: str
    password: str
    active: bool


class TokenPayload(BaseModel):
    sub: str
    exp: int


class JWT(BaseModel):
    secret: str
    algorithm: str
    expire_minutes: int
