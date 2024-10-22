from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict, BaseSettings


class HashConfig(BaseModel):
    n: int = 16384
    r: int = 8
    p: int = 1


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080


class DBConfig(BaseModel):
    host: str
    port: int = 5432
    user: str
    password: str
    dbname: str

    @property
    def connection_url(self):
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}'


class CORSConfig(BaseModel):
    allow_origins: list[str]
    allow_credentials: bool = True
    allow_headers: list[str] = ["*"]
    allow_methods: list[str] = ["*"]


class RedisConfig(BaseModel):
    url: str


class AuthConfig(BaseModel):
    session_lifetime_hours: int = 24


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore"
    )

    run: RunConfig = RunConfig()
    db: DBConfig
    hash: HashConfig = HashConfig()

    cors: CORSConfig
    redis: RedisConfig

    auth: AuthConfig = AuthConfig()


_settings = None


def get_settings() -> Settings:
    global _settings
    if not _settings:
        _settings = Settings()
    return _settings
