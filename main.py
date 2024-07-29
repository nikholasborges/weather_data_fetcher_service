from fastapi import FastAPI
from weather_data_fetcher_service.rest.routes import app1, app2

app = FastAPI()

app.mount("/api/v1", app1)
app.mount("/api/v2", app2)
