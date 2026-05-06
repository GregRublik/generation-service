from pydantic_settings import BaseSettings, SettingsConfigDict
from aiohttp import ClientSession

class SessionManager:
    _session: ClientSession | None = None

    @classmethod
    async def get_session(cls) -> ClientSession:
        """Возвращает сессию aiohttp, создавая её при первом вызове."""
        if cls._session is None or cls._session.closed:
            cls._session = ClientSession()
        return cls._session

    @classmethod
    async def close_session(cls):
        """Закрывает сессию, если она существует."""
        if cls._session is not None:
            await cls._session.close()
            cls._session = None

class DBSettings(BaseSettings):
    host: str
    user: str
    password: str
    name: str
    port: int

    model_config = SettingsConfigDict(env_prefix="DB_", env_file=".env", extra="ignore")

    @property
    def dsn_asyncpg(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class LLMSettings(BaseSettings):
    host: str
    port: int

    model_config = SettingsConfigDict(env_prefix="LLM_", env_file=".env", extra="ignore")

    @property
    def dsn(self):
        return f"http://{self.host}:{self.port}"


class Settings(BaseSettings):
    host: str
    port: int

    db: DBSettings
    llm: LLMSettings

    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env", extra="ignore")


settings = Settings(
    db=DBSettings(),
    llm=LLMSettings(),
)