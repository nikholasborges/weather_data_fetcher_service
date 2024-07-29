from pydantic import BaseModel
from weather_data_fetcher_service.core.logger import logger


class BaseProcess:

    def __init__(self, process_data: BaseModel):
        self.process_data = process_data
        self.logger = logger
        self.log_identifier = f"[Process ID: {self.process_data.process_id}] -"

    def execute(self):
        raise NotImplementedError("Method 'execute' must be implemented in subclass")


class ProcessResponse:

    def __init__(self, status: bool, message: str, data: dict = None):
        self.status = status
        self.message = message
        self.data = data
