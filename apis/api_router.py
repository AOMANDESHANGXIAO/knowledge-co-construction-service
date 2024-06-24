from apis.router.classroom import classroom_router
from apis.router.student import user_router
from apis.router.group import group_router
from apis.router.discussion import discussion_router

routers = [classroom_router, user_router, group_router, discussion_router]
