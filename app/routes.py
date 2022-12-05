from fastapi import APIRouter
from app.users import router as user_router
from app.posts import router as post_router

api_router = APIRouter()

api_router.include_router(
    user_router, tags=["user"], prefix="/user")

api_router.include_router(
    post_router, tags=["posts"], prefix="/posts")
