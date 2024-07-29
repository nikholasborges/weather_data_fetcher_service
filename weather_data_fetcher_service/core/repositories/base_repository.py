from abc import ABC, abstractmethod


class BaseRepository(ABC):

    @abstractmethod
    def fetch_json_data(self, id: int):
        raise NotImplementedError

    @abstractmethod
    def save_json_data(self, id: int, data: dict):
        raise NotImplementedError
