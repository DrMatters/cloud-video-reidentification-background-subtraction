from passlib.context import CryptContext
from google.cloud import datastore

from exceptions import InvalidCredentials
from models import User


class UserManager:
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def __init__(self, db: datastore.Client):
        self.db = db

    def register_user(self, username, password) -> User:
        hashed_password = self.pwd_context.hash(password)

        key = datastore.Key('User')
        user = datastore.Entity(key)
        user.update({
            'username': username,
            'password': hashed_password,
        })

        self.db.put(hashed_password)

        return User(**user)

    def get_user(self, username: str) -> User:
        query = self.db.query(kind='User')
        query.add_filter('username', '=', username)
        results = list(query.fetch(1))
        if len(results) == 1:
            return User(**dict(results[0]))
        else:
            raise InvalidCredentials()

    def authenticate_user(self, username: str, password: str) -> User:
        user = self.get_user(username)
        if not user:
            raise InvalidCredentials()
        if not self.pwd_context.verify(password, user.password):
            raise InvalidCredentials()

        return user
