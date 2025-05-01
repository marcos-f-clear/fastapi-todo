from fastapi import APIRouter
from apis.v1 import auth
from apis.v1 import users
from apis.v1 import tasks

api_router = APIRouter()
api_router.include_router(users.router, prefix="", tags=["users"])
api_router.include_router(tasks.router, prefix="", tags=["tasks"])
api_router.include_router(auth.router, prefix="", tags=["auth"])
