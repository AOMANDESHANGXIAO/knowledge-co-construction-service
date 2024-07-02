from apis.router.user.classroom import classroom_router
from apis.router.user.student import user_router
from apis.router.user.group import group_router
from apis.router.user.discussion import discussion_router
from apis.router.user.flow import flow_router
from apis.router.admin.sign import admin_sign_router
from apis.router.admin._class import _class_router
from apis.router.admin.discussion import admin_discussion_router

routers = [
    classroom_router,
    user_router,
    group_router,
    discussion_router,
    flow_router,
    admin_sign_router,
    _class_router,
    admin_discussion_router
]
