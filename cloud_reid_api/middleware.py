from starlette.middleware.base import BaseHTTPMiddleware

from model_managers.comment import CommentManager
from model_managers.group import GroupManager
from model_managers.user import UserManager
from vkapi import VKAPI


class DatabaseMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, db):
        super().__init__(app)
        self.db = db
        self.user_manager = UserManager(db)
        self.group_manager = GroupManager(db)
        self.comment_manager = CommentManager(db)

    async def dispatch(self, request, call_next):
        request.state.users = self.user_manager
        request.state.groups = self.group_manager
        request.state.comments = self.comment_manager

        return await call_next(request)


class VKAPIMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, key: str):
        super().__init__(app)

        self.vk_api = VKAPI(key)

    async def dispatch(self, request, call_next):
        request.state.vk = self.vk_api

        return await call_next(request)
