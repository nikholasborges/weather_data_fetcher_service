import json
import redis
from weather_data_fetcher_service.core import settings
from weather_data_fetcher_service.core.repositories.base_repository import (
    BaseRepository,
)


class RedisRepository(BaseRepository):
    def __init__(self):
        self._redis = redis.Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
        )

    async def fetch_json_data(self, id: int) -> str:
        data = self._redis.json().get(id)
        return json.loads(data) if data else None

    async def save_json_data(self, id: int, data: dict, path: str = "."):
        self._redis.json().set(id, path=path, obj=data)
