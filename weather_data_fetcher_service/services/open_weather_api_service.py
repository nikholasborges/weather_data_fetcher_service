import aiohttp
import traceback
from typing import List

from weather_data_fetcher_service.services.base_weather_api_service import (
    BaseWeatherAPIService,
)
from weather_data_fetcher_service.core.constants import WeatherAPIConstants
from weather_data_fetcher_service.core import settings
from weather_data_fetcher_service.core.logger import logger


class OpenWeatherAPIService(BaseWeatherAPIService):

    def __init__(self, log_identifier: str):
        self.log_identifier = log_identifier
        self.base_url = settings.OPEN_WEATHER_BASE_URL
        self.api_key = settings.OPEN_WEATHER_API_KEY

        self.group_endpoint = "/group"
        self.cities_per_minute = WeatherAPIConstants.OPEN_WEATHER_CITIES_PER_MINUTE
        self.cities_per_request = WeatherAPIConstants.OPEN_WEATHER_CITIES_PER_REQUEST

    def format_city_id_list(self, city_ids: List[str]):
        try:
            return ",".join(city_ids)
        except TypeError:
            logger.error(
                f"{self.log_identifier} - city_ids list must be string: {city_ids}"
            )
            raise TypeError

    def filter_relevant_data(self, response: dict):
        try:
            return {
                "city_id": response["id"],
                "temperature": response["main"]["temp"],
                "humidity": response["main"]["humidity"],
            }
        except KeyError:
            logger.error(
                f"{self.log_identifier} - Incorrect fields provided in response: {response}"
            )
            raise KeyError

    async def fetch_data_in_bulk(self, city_ids: List[str]):
        try:

            temp_unit = WeatherAPIConstants.OPEN_WEATHER_METRIC_TEMP_UNITS
            formatted_city_ids = self.format_city_id_list(city_ids)

            full_url = (
                f"{self.base_url}{self.group_endpoint}"
                f"?id={formatted_city_ids}&appid={self.api_key}&units={temp_unit}"
            )

            async with aiohttp.ClientSession() as session:
                async with session.get(full_url) as response:

                    if not response.status == 200:
                        logger.error(
                            f"{self.log_identifier} - request wasn't sucessful. "
                            f"Status code: {response.status} "
                            f"Message: {response.message}"
                        )
                        return False

                    data = await response.json()

                    return [
                        self.filter_relevant_data(city_data)
                        for city_data in data["list"]
                    ]

        except TimeoutError as e:
            logger.error(f"{self.log_identifier} - Timeout error occurred: {e}")
            return False

        except Exception as e:
            logger.error(f"{self.log_identifier} - An error occurred: {e}")
            logger.error(f"{self.log_identifier} - Traceback: {traceback.format_exc()}")
            return False
