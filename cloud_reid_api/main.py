import uvicorn
from fastapi import FastAPI, Depends
from google.cloud.datastore import Client
from starlette.middleware.cors import CORSMiddleware

from auth import get_current_active_user
from exceptions import InvalidToken, InvalidCredentials, EntityNotFound
from handlers import auth_router, router
from middleware import DatabaseMiddleware, VKAPIMiddleware
from os import getenv

from exception_handlers import expired_signature_exception_handler, wrong_credentials, entity_not_found

PROJECT_ID = getenv('GCP_PROJECT')
API_KEY = getenv('API_KEY')
ORIGINS = getenv('ORIGINS', '').split(',')

app = FastAPI(title='ai_moderator_api')


app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(router, prefix='/api/v1')
app.include_router(auth_router, prefix='/api/v1', dependencies=[Depends(get_current_active_user)])

app.add_exception_handler(InvalidCredentials, expired_signature_exception_handler)
app.add_exception_handler(InvalidToken, wrong_credentials)
app.add_exception_handler(EntityNotFound, entity_not_found)

datastore_client = Client()
app.add_middleware(DatabaseMiddleware, db=datastore_client)
app.add_middleware(VKAPIMiddleware, key=API_KEY)

if __name__ == "__main__":
    uvicorn.run(app, port=8080, log_level='debug')
