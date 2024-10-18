from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.root import root_router


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
