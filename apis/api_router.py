from apis.router.user.classroom import classroom_router
from apis.router.user.student import user_router
from apis.router.user.group import group_router
from apis.router.user.discussion import discussion_router
from apis.router.user.flow import flow_router

routers = [classroom_router, user_router, group_router, discussion_router, flow_router]
