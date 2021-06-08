from starlette.requests import Request


def get_user_manager(request: Request):
    return request.state.users


def get_group_manager(request: Request):
    return request.state.groups


def get_comment_manager(request: Request):
    return request.state.comments


def get_vk(request: Request):
    return request.state.vk
