import uvicorn

from app import App
from config import get_settings

app = App()
settings = get_settings()


if __name__ == "__main__":
    uvicorn.run(app, host=settings.run.host, port=settings.run.port)