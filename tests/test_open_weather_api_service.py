import pytest
from unittest.mock import AsyncMock, patch

from weather_data_fetcher_service.services.open_weather_api_service import (
    OpenWeatherAPIService,
)
from weather_data_fetcher_service.core.constants import WeatherAPIConstants
from weather_data_fetcher_service.core import settings


@pytest.fixture
def open_weather_api_service():
    return OpenWeatherAPIService(log_identifier="test_log")


@pytest.mark.asyncio
async def test_format_city_id_list(open_weather_api_service):
    city_ids = ["123", "456", "789"]
    formatted_city_ids = open_weather_api_service.format_city_id_list(city_ids)
    assert formatted_city_ids == "123,456,789"


@pytest.mark.asyncio
async def test_filter_relevant_data(open_weather_api_service):
    response = {"id": 123, "main": {"temp": 25, "humidity": 80}}
    filtered_data = open_weather_api_service.filter_relevant_data(response)
    assert filtered_data == {"city_id": 123, "temperature": 25, "humidity": 80}


@pytest.mark.asyncio
@patch("weather_data_fetcher_service.core.logger.StreamLogger.error")
async def test_format_city_id_list_non_string_ids(
    mock_logger_error, open_weather_api_service
):
    city_ids = [123, 456, 789]
    with pytest.raises(TypeError):
        open_weather_api_service.format_city_id_list(city_ids)
    mock_logger_error.assert_called_once_with(
        "test_log - city_ids list must be string: [123, 456, 789]"
    )


@pytest.mark.asyncio
@patch("weather_data_fetcher_service.core.logger.StreamLogger.error")
async def test_filter_relevant_data_missing_fields(
    mock_logger_error, open_weather_api_service
):
    response = {"id": 123, "main": {}}
    with pytest.raises(KeyError):
        open_weather_api_service.filter_relevant_data(response)
    mock_logger_error.assert_called_once_with(
        "test_log - Incorrect fields provided in response: {'id': 123, 'main': {}}"
    )


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_fetch_data_in_bulk_success(
    mock_client_session, open_weather_api_service
):

    try:

        json_respone = AsyncMock(
            return_value={
                "list": [
                    {"id": 123, "main": {"temp": 25, "humidity": 80}},
                    {"id": 456, "main": {"temp": 20, "humidity": 75}},
                    {"id": 789, "main": {"temp": 18, "humidity": 70}},
                ]
            }
        )

        mock_client_session.return_value.__aenter__.return_value.status = 200
        mock_client_session.return_value.__aenter__.return_value.message = "Success"
        mock_client_session.return_value.__aenter__.return_value.json = json_respone

        city_ids = ["123", "456", "789"]
        response_data = await open_weather_api_service.fetch_data_in_bulk(city_ids)
        assert response_data == [
            {"city_id": 123, "temperature": 25, "humidity": 80},
            {"city_id": 456, "temperature": 20, "humidity": 75},
            {"city_id": 789, "temperature": 18, "humidity": 70},
        ]

        mock_client_session.assert_called_once()

    except Exception as e:
        assert False, f"Test failed with exception: {e}"


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
@patch("weather_data_fetcher_service.core.logger.StreamLogger.error")
async def test_fetch_data_in_bulk_failure(
    mock_logger, mock_client_session, open_weather_api_service
):

    try:

        mock_client_session.return_value.__aenter__.return_value.status = 404
        mock_client_session.return_value.__aenter__.return_value.message = "Not Found"

        city_ids = ["123", "456", "789"]
        response = await open_weather_api_service.fetch_data_in_bulk(city_ids)

        assert response is False
        mock_client_session.assert_called_once()
        mock_logger.assert_any_call(
            "test_log - request wasn't sucessful. Status code: 404 Message: Not Found"
        )

    except Exception as e:
        assert False, f"Test failed with exception: {e}"


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
@patch("weather_data_fetcher_service.core.logger.StreamLogger.error")
async def test_fetch_data_in_bulk_timeout(
    mock_logger, mock_client_session, open_weather_api_service
):

    mock_client_session.return_value.__aenter__.side_effect = TimeoutError(
        "TimeoutError"
    )

    city_ids = ["123", "456", "789"]
    response = await open_weather_api_service.fetch_data_in_bulk(city_ids)

    assert response is False
    mock_client_session.assert_called_once()
    mock_logger.assert_any_call("test_log - Timeout error occurred: TimeoutError")


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
@patch("weather_data_fetcher_service.core.logger.StreamLogger.error")
async def test_fetch_data_in_bulk_exception(
    mock_logger, mock_client_session, open_weather_api_service
):

    mock_client_session.return_value.__aenter__.side_effect = Exception("Error")

    city_ids = ["123", "456", "789"]
    response = await open_weather_api_service.fetch_data_in_bulk(city_ids)

    assert response is False
    mock_client_session.assert_called_once()
    mock_logger.assert_any_call("test_log - An error occurred: Error")


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
@patch("weather_data_fetcher_service.core.logger.StreamLogger.error")
async def test_fetch_data_in_bulk_empty_api_key(
    mock_logger_error, mock_client_session, open_weather_api_service
):
    with patch.object(settings, "OPEN_WEATHER_API_KEY", ""):
        json_response = AsyncMock(return_value={"list": []})
        mock_client_session.return_value.__aenter__.return_value.status = 401
        mock_client_session.return_value.__aenter__.return_value.message = (
            "Unauthorized"
        )
        mock_client_session.return_value.__aenter__.return_value.json = json_response

        city_ids = ["123", "456", "789"]
        response = await open_weather_api_service.fetch_data_in_bulk(city_ids)

        assert response is False
        mock_client_session.assert_called_once()
        mock_logger_error.assert_called_with(
            "test_log - request wasn't sucessful. Status code: 401 Message: Unauthorized"
        )


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
@patch("weather_data_fetcher_service.core.logger.StreamLogger.error")
async def test_fetch_data_in_bulk_misconfigured_base_url(
    mock_logger_error, mock_client_session, open_weather_api_service
):
    with patch.object(settings, "OPEN_WEATHER_BASE_URL", "http://invalid-url"):
        json_response = AsyncMock(return_value={"list": []})
        mock_client_session.return_value.__aenter__.return_value.status = 404
        mock_client_session.return_value.__aenter__.return_value.message = "Not Found"
        mock_client_session.return_value.__aenter__.return_value.json = json_response

        city_ids = ["123", "456", "789"]
        response = await open_weather_api_service.fetch_data_in_bulk(city_ids)

        assert response is False
        mock_client_session.assert_called_once()
        mock_logger_error.assert_called_with(
            "test_log - request wasn't sucessful. Status code: 404 Message: Not Found"
        )


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
@patch("weather_data_fetcher_service.core.logger.StreamLogger.error")
async def test_fetch_data_in_bulk_missing_temp_unit(
    mock_logger_error, mock_client_session, open_weather_api_service
):
    with patch.object(WeatherAPIConstants, "OPEN_WEATHER_METRIC_TEMP_UNITS", None):

        mock_client_session.return_value.__aenter__.return_value.status = 404
        mock_client_session.return_value.__aenter__.return_value.message = "Not Found"

        city_ids = ["123", "456", "789"]
        response = await open_weather_api_service.fetch_data_in_bulk(city_ids)

        assert response is False
        mock_client_session.assert_called_once()
        mock_logger_error.assert_called_with(
            "test_log - request wasn't sucessful. Status code: 404 Message: Not Found"
        )


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
@patch("weather_data_fetcher_service.core.logger.StreamLogger.error")
async def test_fetch_data_in_bulk_exceed_cities_per_request(
    mock_logger_error, mock_client_session, open_weather_api_service
):
    with patch.object(WeatherAPIConstants, "OPEN_WEATHER_CITIES_PER_REQUEST", 2):

        mock_client_session.return_value.__aenter__.return_value.status = 408
        mock_client_session.return_value.__aenter__.return_value.message = (
            "Exceeded cities per request limit"
        )

        city_ids = ["123", "456", "789"]
        response = await open_weather_api_service.fetch_data_in_bulk(city_ids)

        assert response is False
        mock_logger_error.assert_called_with(
            "test_log - request wasn't sucessful. Status code: 408 Message: Exceeded cities per request limit"
        )
