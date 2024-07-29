from pydantic import BaseModel
from typing import Optional


class CityWeatherProcessData(BaseModel):
    process_id: int
    request_datetime: Optional[str] = None
    cities_ids: Optional[list] = None
    total_cities: Optional[int] = None
    results: Optional[list] = None

    def to_json(self):
        return self.model_dump_json()
