from fastapi import APIRouter, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm

from auth import create_access_token, get_current_user
from dependencies import get_user_manager, get_group_manager, get_comment_manager, get_vk
from model_managers.comment import CommentManager, Rate, Sort
from model_managers.group import GroupManager
from model_managers.user import UserManager
from models import User
from vkapi import VKAPI

router = APIRouter()
auth_router = APIRouter()


@router.post('/authorize', tags=['auth'])
def login(user_manager: UserManager = Depends(get_user_manager),
          form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_manager.authenticate_user(form_data.username, form_data.password)
    token = create_access_token(user.username)
    return {
        'status': 'ok',
        'token': token,
    }


@auth_router.get('/get_user')
def get_user(user: User = Depends(get_current_user)):
    return {
        'status': 'ok',
        'payload': {
            user.username,
        },
    }


@auth_router.get('/groups', tags=['groups'])
async def get_groups(group_manager: GroupManager = Depends(get_group_manager), vk: VKAPI = Depends(get_vk)):
    groups = group_manager.get_groups()
    groups = await vk.get_groups_by_id(*[group['id'] for group in groups])

    return {
        'status': 'ok',
        'payload': groups,
    }


@auth_router.get('/groups/{group_id}', tags=['groups'])
def get_group(group_id: int,
              group_manager: GroupManager = Depends(get_group_manager)):
    group = group_manager.get_group(group_id)

    return {
        'status': 'ok',
        'payload': group,
    }


@auth_router.get('/groups/{group_id}/comments', tags=['comments'])
def get_comments(group_id: int,
                 limit: int = None,
                 offset: int = 0,
                 rate: Rate = None,
                 sort: Sort = None,
                 comment_manager: CommentManager = Depends(get_comment_manager)):
    comments = comment_manager.get_comments(group_id, limit, offset, rate, sort)

    return {
        'status': 'ok',
        'payload': comments,
    }


@auth_router.get('/groups/{group_id}/comments/{comment_id}', tags=['comments'])
def get_comment(group_id: int,
                comment_id: int,
                comment_manager: CommentManager = Depends(get_comment_manager)):
    comment = comment_manager.get_comment(group_id, comment_id)

    return {
        'status': 'ok',
        'payload': comment,
    }


@auth_router.post('/groups/{group_id}/comments/{comment_id}/rate', tags=['comments'])
def rate_comment(group_id: int,
                 comment_id: int,
                 rate: Rate = Body(..., embed=True),
                 comment_manager: CommentManager = Depends(get_comment_manager)):
    comment = comment_manager.rate_comment(group_id, comment_id, rate)

    return {
        'status': 'ok',
        'payload': comment,
    }
