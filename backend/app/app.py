from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.root import root_router
from config import get_settings

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        pass  # close resources


class App(FastAPI):
    def __init__(self, **kwargs):
        super().__init__(**(kwargs | {"lifespan": lifespan}))

        self.include_router(root_router)

        self.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors.allow_origins,
            allow_credentials=settings.cors.allow_credentials,
            allow_methods=settings.cors.allow_methods,
            allow_headers=settings.cors.allow_headers,
        )