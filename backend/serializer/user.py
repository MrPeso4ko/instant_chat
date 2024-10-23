from pydantic import BaseModel, ConfigDict


class UserAuth(BaseModel):
    username: str
    password: str


class BaseUser(BaseModel):
    name: str


class BaseUserGet(BaseUser):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ExtendedUser(BaseUser):
    username: str


class UserCreate(ExtendedUser):
    password: str


class UserGet(ExtendedUser):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserDB(ExtendedUser):
    model_config = ConfigDict(from_attributes=True)

    hashed_password: bytes
    salt: bytes


class UserCreateDB(UserDB):
    pass


class UserGetDB(UserDB):
    id: int
