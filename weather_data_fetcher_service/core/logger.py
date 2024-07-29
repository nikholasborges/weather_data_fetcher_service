import logging


class StreamLogger:
    def __init__(self, name: str, level: int = logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self._setup_stream_handler()

    def _setup_stream_handler(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)


logger = StreamLogger("weather_data_fetcher_service")
