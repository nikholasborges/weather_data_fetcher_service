from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from weather_data_fetcher_service.rest.routes import app1, app2

app = FastAPI(
    title="Weather Data Fetcher Service",
    description="A FastAPI-based service for fetching and processing weather data.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/api/v1", app1)
app.mount("/api/v2", app2)
