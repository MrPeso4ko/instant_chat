from pydantic import BaseModel


def exception_model(detail_str: str):
    class Model(BaseModel):
        detail: str = detail_str

    return {"model": Model}


def status_model(status_str: str):
    class Model(BaseModel):
        status: str = status_str

    return {"model": Model}
