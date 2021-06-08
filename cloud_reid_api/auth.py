from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from google.cloud import datastore
from google.cloud.datastore import Client

from dependencies import get_user_manager
from exceptions import EntityNotFound, InvalidToken
from model_managers.user import UserManager
from models import TokenPayload, JWT

JWT_ID = 5644406560391168


def get_jwt(db: datastore.Client, jwt_id: int):
    jwt_key = db.key('JWT', jwt_id)
    jwt_info = JWT(**db.get(jwt_key))
    return jwt_info


datastore_client = Client()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/authorize")
jwt_info = get_jwt(datastore_client, JWT_ID)


def create_access_token(login: str, expires_delta: timedelta = timedelta(minutes=15)):
    expire = datetime.utcnow() + expires_delta
    claims = {
        'sub': login,
        'exp': expire,
    }

    return jwt.encode(claims, jwt_info.secret, algorithm=jwt_info.algorithm)


def get_current_user(user_manager: UserManager = Depends(get_user_manager),
                     token: str = Depends(oauth2_scheme)):
    try:
        payload = TokenPayload(**jwt.decode(token, jwt_info.secret, algorithms=[jwt_info.algorithm]))
    except jwt.PyJWTError as e:
        raise InvalidToken(e)

    user = user_manager.get_user(payload.sub)
    if user is None:
        raise EntityNotFound('User not found')

    return user


def get_current_active_user(current_user=Depends(get_current_user)):
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
