from dataclasses import dataclass
from typing import Any


@dataclass
class Comment:
    post_id: int
    text: str
    owner_id: int
    post_owner_id: int
    id: int
    known_class: int
    date: int
    predicted_probability: float
    thread: Any
    from_id: int
    group_id: int
    parents_stack: Any


@dataclass
class Group:
    id: int
    base_folder_path: str
    framework: str
    preprocessing_version: str


@dataclass
class User:
    username: str
    password: str
    active: bool


@dataclass
class TokenPayload:
    sub: str
    exp: int


@dataclass
class JWT:
    secret: str
    algorithm: str
    expire_minutes: int
