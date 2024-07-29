import pytest
from unittest.mock import AsyncMock, MagicMock

from weather_data_fetcher_service.process.base_process import ProcessResponse
from weather_data_fetcher_service.core.models.weather_data_models import (
    CityWeatherProcessData,
)
from weather_data_fetcher_service.services.base_weather_api_service import (
    BaseWeatherAPIService,
)
from weather_data_fetcher_service.core.repositories.base_repository import (
    BaseRepository,
)
from weather_data_fetcher_service.process.weather_data_process import (
    UploadCityListProcesser,
    CityWeatherDataProcesser,
    CityWeatherDataFetcher,
)  # Replace 'your_module' with the actual module name


@pytest.fixture
def mock_repository():
    repo = AsyncMock(spec=BaseRepository)
    repo.save_json_data = AsyncMock()
    repo.fetch_json_data = AsyncMock()
    return repo


@pytest.fixture
def mock_weather_api_service():
    service = AsyncMock(spec=BaseWeatherAPIService)
    service.fetch_data_in_bulk = AsyncMock()
    return service


@pytest.fixture
def upload_city_list_processor(mock_repository):
    process_data = CityWeatherProcessData(process_id=1, cities_ids=[1, 2, 3])
    processor = UploadCityListProcesser(process_data, lambda: mock_repository)
    processor.logger = MagicMock()
    return processor


@pytest.fixture
def city_weather_data_processor(mock_weather_api_service, mock_repository):
    process_data = CityWeatherProcessData(process_id=1, cities_ids=[1, 2, 3])
    processor = CityWeatherDataProcesser(
        lambda _: mock_weather_api_service, lambda: mock_repository, process_data
    )
    processor.logger = MagicMock()
    return processor


@pytest.fixture
def city_weather_data_fetcher(mock_repository):
    process_data = CityWeatherProcessData(process_id=1, cities_ids=[1, 2, 3])
    fetcher = CityWeatherDataFetcher(lambda: mock_repository, process_data)
    fetcher.logger = MagicMock()
    return fetcher


@pytest.mark.asyncio
async def test_save_city_list(upload_city_list_processor, mock_repository):
    await upload_city_list_processor.save_city_list()
    mock_repository.save_json_data.assert_called_once_with(
        id=upload_city_list_processor.process_data.process_id,
        data=upload_city_list_processor.process_data.to_json(),
    )


@pytest.mark.asyncio
async def test_upload_city_list_processor_execute_success(
    upload_city_list_processor, mock_repository
):
    response = await upload_city_list_processor.execute()
    mock_repository.save_json_data.assert_called_once()
    upload_city_list_processor.logger.info.assert_called_with(
        f"{upload_city_list_processor.log_identifier} Data Uploaded successfully."
    )

    assert response.status == 200
    assert response.message == "Data Uploaded successfully."


@pytest.mark.asyncio
async def test_upload_city_list_processor_execute_failure(
    upload_city_list_processor, mock_repository
):
    mock_repository.save_json_data.side_effect = Exception("Error")
    response = await upload_city_list_processor.execute()
    upload_city_list_processor.logger.error.assert_called()

    assert response.status == 500
    assert response.message == "An internal error occurred."


@pytest.mark.asyncio
async def test_city_weather_data_processor_get_stored_process_data(
    city_weather_data_processor, mock_repository
):
    await city_weather_data_processor.get_stored_process_data(
        city_weather_data_processor.process_data.process_id
    )
    mock_repository.fetch_json_data.assert_called_once_with(
        city_weather_data_processor.process_data.process_id
    )


@pytest.mark.asyncio
async def test_city_weather_data_processor_store_data(
    city_weather_data_processor, mock_repository
):
    await city_weather_data_processor.store_data(
        city_weather_data_processor.process_data.process_id, {}
    )
    mock_repository.save_json_data.assert_called_once_with(
        city_weather_data_processor.process_data.process_id, {}
    )


@pytest.mark.asyncio
async def test_city_weather_data_processor_get_weather_data(
    city_weather_data_processor, mock_weather_api_service
):
    await city_weather_data_processor.get_weather_data([1, 2, 3])
    mock_weather_api_service.fetch_data_in_bulk.assert_called_once_with([1, 2, 3])


@pytest.mark.asyncio
async def test_city_weather_data_processor_execute_success(
    city_weather_data_processor, mock_weather_api_service, mock_repository
):
    mock_weather_api_service.cities_per_minute = 60
    mock_weather_api_service.cities_per_request = 20
    mock_repository.fetch_json_data.return_value = {"cities_ids": [1, 2, 3]}
    mock_weather_api_service.fetch_data_in_bulk.return_value = [
        {"city": 1},
        {"city": 2},
        {"city": 3},
    ]

    response = await city_weather_data_processor.execute()
    mock_repository.save_json_data.assert_called()
    city_weather_data_processor.logger.info.assert_any_call(
        f"{city_weather_data_processor.log_identifier} Process finished successfully."
    )

    assert response.status == 200
    assert response.message == "Process finished successfully."


@pytest.mark.asyncio
async def test_city_weather_data_processor_execute_no_data(
    city_weather_data_processor, mock_repository
):
    mock_repository.fetch_json_data.return_value = None

    response = await city_weather_data_processor.execute()
    city_weather_data_processor.logger.error.assert_called_with(
        f"{city_weather_data_processor.log_identifier} No stored city list found "
    )

    assert response.status == 404
    assert response.message == "No data found."


@pytest.mark.asyncio
async def test_city_weather_data_processor_execute_failure(
    city_weather_data_processor, mock_repository
):
    mock_repository.fetch_json_data.side_effect = Exception("Error")

    response = await city_weather_data_processor.execute()
    city_weather_data_processor.logger.error.assert_called()

    assert response.status == 500
    assert response.message == "An internal error occurred."


@pytest.mark.asyncio
async def test_city_weather_data_fetcher_fetch_data(
    city_weather_data_fetcher, mock_repository
):
    await city_weather_data_fetcher.fetch_data(
        city_weather_data_fetcher.process_data.process_id
    )
    mock_repository.fetch_json_data.assert_called_once_with(
        city_weather_data_fetcher.process_data.process_id
    )


@pytest.mark.asyncio
async def test_city_weather_data_fetcher_execute_success(
    city_weather_data_fetcher, mock_repository
):
    mock_repository.fetch_json_data.return_value = {
        "process_id": 1,
        "request_datetime": "2024-07-29T00:00:00",
        "total_cities": 3,
        "results": [{"city": 1}, {"city": 2}, {"city": 3}],
    }

    response = await city_weather_data_fetcher.execute()
    city_weather_data_fetcher.logger.info.assert_called_with(
        f"{city_weather_data_fetcher.log_identifier} Data fetched successfully."
    )
    assert response.status == 200
    assert response.message == "Data fetched successfully."
    assert "progress_percent" in response.data


@pytest.mark.asyncio
async def test_city_weather_data_fetcher_execute_no_data(
    city_weather_data_fetcher, mock_repository
):
    mock_repository.fetch_json_data.return_value = None

    response = await city_weather_data_fetcher.execute()
    city_weather_data_fetcher.logger.error.assert_called_with(
        f"{city_weather_data_fetcher.log_identifier} No processed data found."
    )

    assert response.status == 404
    assert response.message == "No processed data found."


@pytest.mark.asyncio
async def test_city_weather_data_fetcher_execute_failure(
    city_weather_data_fetcher, mock_repository
):
    mock_repository.fetch_json_data.side_effect = Exception("Error")

    response = await city_weather_data_fetcher.execute()
    city_weather_data_fetcher.logger.error.assert_called()

    assert response.status == 500
    assert response.message == "An internal error occurred."
