from abc import ABC, abstractmethod


class BaseWeatherAPIService(ABC):

    def __init__(self, log_identifier: str):
        self.log_identifier
        self.base_url
        self.endpoint
        self.api_key
        self.cities_per_minute
        self.cities_per_request

    @abstractmethod
    def filter_relevant_data(self, response: dict):
        raise NotImplementedError

    @abstractmethod
    async def fetch_data_in_bulk(self, id_list: str):
        raise NotImplementedError
