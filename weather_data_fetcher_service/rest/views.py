from datetime import datetime
from fastapi.responses import JSONResponse

from weather_data_fetcher_service.core.models.weather_data_models import (
    CityWeatherProcessData,
)
from weather_data_fetcher_service.process.weather_data_process import (
    UploadCityListProcesser,
    CityWeatherDataProcesser,
    CityWeatherDataFetcher,
)
from weather_data_fetcher_service.services.open_weather_api_service import (
    OpenWeatherAPIService,
)
from weather_data_fetcher_service.core.repositories.redis_repository import (
    RedisRepository,
)


async def upload_city_list_view(parameters):
    """
    Upload a list of city IDs for weather data processing.

    Args:
        parameters (UploadParameter): The parameters containing process_id and list of city IDs.

    Returns:
        JSONResponse: A JSON response with the status and message.
    """

    process_data = CityWeatherProcessData(
        process_id=parameters.process_id,
        cities_ids=parameters.cities_ids,
    )

    process = UploadCityListProcesser(
        process_data=process_data, repository=RedisRepository
    )

    response = await process.execute()

    return JSONResponse(
        status_code=response.status, content={"message": response.message}
    )


async def process_city_data_view(parameters):
    """
    Process weather data for a list of cities in bulk.

    Args:
        parameters (ProcessParameter): The parameters containing the process_id.

    Returns:
        JSONResponse: A JSON response with the status and message.
    """

    request_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    process_data = CityWeatherProcessData(
        request_datetime=request_datetime,
        process_id=parameters.process_id,
    )

    process = CityWeatherDataProcesser(
        weather_API_service=OpenWeatherAPIService,
        repository=RedisRepository,
        process_data=process_data,
    )

    response = await process.execute()

    return JSONResponse(
        status_code=response.status, content={"message": response.message}
    )


async def get_city_data_view(parameters):
    """
    Fetch the processed weather data for a specific process ID.

    Args:
        parameters (dict): The parameters containing the process_id.

    Returns:
        JSONResponse: A JSON response with the status and the data or message.
    """
    process_data = CityWeatherProcessData(process_id=parameters.get("process_id"))

    process = CityWeatherDataFetcher(
        repository=RedisRepository, process_data=process_data
    )

    response = await process.execute()
    content = response.data if response.data else {"message": response.message}

    return JSONResponse(status_code=response.status, content=content)
