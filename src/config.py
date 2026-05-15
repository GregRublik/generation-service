from pydantic_settings import BaseSettings, SettingsConfigDict


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
    api_key: str
    model_name: str

    model_config = SettingsConfigDict(env_prefix="LLM_", env_file=".env", extra="ignore")

    @property
    def dsn_http(self):
        return f"http://{self.host}:{self.port}"

    @property
    def dsn_https(self):
        return f"https://{self.host}"


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