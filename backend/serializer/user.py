from pydantic import BaseModel, ConfigDict


class UserAuth(BaseModel):
    username: str
    password: str


class BaseUser(BaseModel):
    name: str
    username: str


class UserCreate(BaseUser):
    password: str


class UserGet(BaseUser):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserDB(BaseUser):
    model_config = ConfigDict(from_attributes=True)

    hashed_password: bytes
    salt: bytes


class UserCreateDB(UserDB):
    pass


class UserGetDB(UserDB):
    id: int
