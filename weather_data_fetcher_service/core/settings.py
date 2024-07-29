from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    OPEN_WEATHER_BASE_URL: str = Field(
        default="https://api.openweathermap.org/data/2.5"
    )
    OPEN_WEATHER_API_KEY: str

    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_DB: int = Field(default=0)

    ROUTE_TIMEOUT_IN_SECONDS: int = Field(default=600)

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")
