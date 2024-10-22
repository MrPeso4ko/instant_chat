import uvicorn

from app import App
from config import get_settings

app = App(openapi_url="/api/openapi.json",
          title="Instant chat API")
settings = get_settings()


if __name__ == "__main__":
    uvicorn.run(app, host=settings.run.host, port=settings.run.port)