import asyncio
import traceback

from weather_data_fetcher_service.process.base_process import (
    BaseProcess,
    ProcessResponse,
)
from weather_data_fetcher_service.services.base_weather_api_service import (
    BaseWeatherAPIService,
)
from weather_data_fetcher_service.core.repositories.base_repository import (
    BaseRepository,
)
from weather_data_fetcher_service.core.models.weather_data_models import (
    CityWeatherProcessData,
)


class UploadCityListProcesser(BaseProcess):

    def __init__(
        self, process_data: CityWeatherProcessData, repository: BaseRepository
    ):
        super().__init__(process_data)
        self.repository = repository()

    async def save_city_list(self):
        return await self.repository.save_json_data(
            id=self.process_data.process_id,
            data=self.process_data.to_json(),
        )

    async def execute(self):

        try:
            await self.save_city_list()

            self.logger.info(f"{self.log_identifier} Data Uploaded successfully.")

            return ProcessResponse(status=200, message="Data Uploaded successfully.")

        except Exception as e:
            self.logger.error(f"{self.log_identifier} An error occurred: {e}")
            self.logger.error(
                f"{self.log_identifier} Traceback: {traceback.format_exc()}"
            )
            return ProcessResponse(status=500, message="An internal error occurred.")


class CityWeatherDataProcesser(BaseProcess):

    def __init__(
        self,
        weather_API_service: BaseWeatherAPIService,
        repository: BaseRepository,
        process_data: CityWeatherProcessData,
    ):
        super().__init__(process_data)
        self.weather_API_service = weather_API_service(self.log_identifier)
        self.repository = repository()

    def prepare_batches(self, cities_ids: list):
        return [
            cities_ids[i : i + self.weather_API_service.cities_per_request]
            for i in range(
                0, len(cities_ids), self.weather_API_service.cities_per_request
            )
        ]

    async def get_stored_process_data(self, process_id: int):
        return await self.repository.fetch_json_data(process_id)

    async def store_data(self, id: int, data: dict):
        return await self.repository.save_json_data(id, data)

    async def get_weather_data(self, cities_ids: list):
        return await self.weather_API_service.fetch_data_in_bulk(cities_ids)

    async def execute(self):

        try:

            self.logger.info(f"{self.log_identifier} Starting process.")

            stored_process_data = await self.get_stored_process_data(
                self.process_data.process_id
            )

            if not stored_process_data or not stored_process_data.get("cities_ids"):
                self.logger.error(f"{self.log_identifier} No stored city list found ")
                return ProcessResponse(status=404, message="No data found.")

            max_requests_per_minute = (
                self.weather_API_service.cities_per_minute
                // self.weather_API_service.cities_per_request
            )

            self.process_data.cities_ids = stored_process_data.get("cities_ids")
            self.process_data.total_cities = len(self.process_data.cities_ids)

            self.logger.info(
                f"{self.log_identifier} {self.process_data.total_cities} cities found to process."
            )

            self.logger.info(f"{self.log_identifier} processing batches...")

            batches = self.prepare_batches(self.process_data.cities_ids)

            results = []
            for i in range(0, len(batches), max_requests_per_minute):

                current_batches = batches[i : i + max_requests_per_minute]
                tasks = [self.get_weather_data(batch) for batch in current_batches]

                batch_results = await asyncio.gather(*tasks)

                for raw_results in batch_results:
                    for result in raw_results:
                        results.append(result)

                self.process_data.results = results

                await self.store_data(
                    self.process_data.process_id, self.process_data.to_json()
                )

                self.logger.info(
                    f"{self.log_identifier} Processed {len(results)} "
                    f"cities out of {self.process_data.total_cities}."
                )

                if i + max_requests_per_minute < len(batches):
                    self.logger.info(
                        f"{self.log_identifier} Waiting a minute before next batch..."
                    )
                    await asyncio.sleep(60)

            self.logger.info(f"{self.log_identifier} Process finished successfully.")

            return ProcessResponse(status=200, message="Process finished successfully.")

        except Exception as e:
            self.logger.error(f"{self.log_identifier} An error occurred: {e}")
            self.logger.error(
                f"{self.log_identifier} Traceback: {traceback.format_exc()}"
            )
            return ProcessResponse(status=500, message="An internal error occurred.")


class CityWeatherDataFetcher(BaseProcess):

    def __init__(
        self, repository: BaseRepository, process_data: CityWeatherProcessData
    ):
        super().__init__(process_data)
        self.repository = repository()

    async def fetch_data(self, process_id: int):
        return await self.repository.fetch_json_data(process_id)

    def format_response(self, data: dict):

        progress_percent = (len(data.get("results")) / data.get("total_cities")) * 100

        return {
            "process_id": data.get("process_id"),
            "request_datetime": data.get("request_datetime"),
            "total_cities": data.get("total_cities"),
            "progress_percent": f"{progress_percent:.2f}%",
            "results": data.get("results"),
        }

    async def execute(self):

        try:

            stored_process_data = await self.fetch_data(self.process_data.process_id)

            if not stored_process_data or not stored_process_data.get("results"):
                self.logger.error(f"{self.log_identifier} No processed data found.")
                return ProcessResponse(status=404, message="No processed data found.")

            self.logger.info(f"{self.log_identifier} Data fetched successfully.")

            return ProcessResponse(
                status=200,
                message="Data fetched successfully.",
                data=self.format_response(stored_process_data),
            )

        except Exception as e:
            self.logger.error(f"{self.log_identifier} - An error occurred: {e}")
            self.logger.error(
                f"{self.log_identifier} - Traceback: {traceback.format_exc()}"
            )
            return ProcessResponse(status=500, message="An internal error occurred.")
