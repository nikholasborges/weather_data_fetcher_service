from fastapi import FastAPI

from weather_data_fetcher_service.core import settings
from weather_data_fetcher_service.rest.views import (
    upload_city_list_view,
    process_city_data_view,
    get_city_data_view,
)
from weather_data_fetcher_service.rest.middlewares import TimeoutMiddleware
from weather_data_fetcher_service.rest.parameters import (
    UploadParameter,
    ProcessParameter,
)

app1 = FastAPI(root_path="/api/v1")
app2 = FastAPI(root_path="/api/v2")
app2.add_middleware(
    TimeoutMiddleware, timeout_seconds=settings.ROUTE_TIMEOUT_IN_SECONDS
)


@app1.post("/upload-city-list")
async def upload_city_list_route(parameters: UploadParameter):
    return await upload_city_list_view(parameters)


@app2.post("/process-city-data-in-bulk")
async def process_city_data_route(parameters: ProcessParameter):
    return await process_city_data_view(parameters)


@app1.get("/get-city-data-process")
async def get_city_data_fetch_route(process_id: int):
    return await get_city_data_view(parameters={"process_id": process_id})
