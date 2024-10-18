from fastapi import APIRouter

from api.auth import auth_router

root_router = APIRouter()

root_router.include_router(auth_router)
