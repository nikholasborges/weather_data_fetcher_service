# Weather Data Fetcher Service

This project is a FastAPI-based application designed to fetch and process weather data in bulk.

## Technologies Used

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
- **Poetry**: Python's dependency management and packaging tool.
- **Docker**: A platform to develop, ship, and run applications in containers.
- **Docker Compose**: A tool for defining and running multi-container Docker applications.
- **Redis Stack**: An in-memory data structure store used as a database, cache, and message broker.
- **Uvicorn**: A lightning-fast ASGI server implementation, using `uvloop` and `httptools`.
- **aiohttp**: An asynchronous HTTP client/server framework for asyncio and Python.

## Prerequisites

- Python 3.11
- Poetry
- Docker
- Docker Compose

By default, this API utilizes OpenWeatherAPI to retrieve weather data. To use this service, please create a free account and generate an API key on the OpenWeatherAPI website: https://openweathermap.org/api.

## Installation

### Clone the Repository

```sh
git clone https://github.com/nikholasborges/weather-data-fetcher-service.git
cd weather-data-fetcher-service
```

### Configure the Environment

The application uses environment variables for configuration. You can set these variables in a `.env` file in the project root. An example `.env` file:

```ini
OPEN_WEATHER_BASE_URL=base_url
OPEN_WEATHER_API_KEY=your_api_key_here
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
ROUTE_TIMEOUT_IN_SECONDS=600
```

### Install Dependencies

Ensure Poetry is installed and then install the dependencies:

```sh
make install
```

## Running the Application

### Run Locally

To run the application locally, first you need to run the Redis Docker container:

```sh
docker run -d -p 6379:6379 redis/redis-stack
```

Then, execute the command below to run the application:

```sh
make run
```

### Run in Development Mode

To run the application in development mode with auto-reload:

```sh
make dev
```

## Testing

Run tests using pytest and generate a coverage report:

```sh
make test
```

## Linting

Lint the code using flake8:

```sh
make lint
```

## Cleaning Up

Clean up the project directory:

```sh
make clean
```

## Docker

### Build and Run as a Docker Container

To build and run the Docker container, execute the code below, this will execute the Redis container and the service container:

```sh
make run-containers
```

To run the containers in detached mode:

```sh
make run-containers-dettached
```

### Stop Docker Containers

To stop the Docker containers (if in detached mode):

```sh
make stop-containers
```

## Documentation

Once the project is running on localhost, you can access the API documentation through the following links:

```
http://localhost:8000/api/v1/docs
http://localhost:8000/api/v2/docs
```

## How to Use the API

### Upload City List

**Endpoint**: `/api/v1/upload-city-list`

**Method**: `POST`

**Description**: Upload a list of city IDs for weather data processing.

**Request Body**:
```json
{
  "process_id": 1,
  "cities_ids": [123, 456, 789]
}
```

**Response**:
```json
{
  "message": "Cities uploaded successfully."
}
```

### Process City Data in Bulk

**Endpoint**: `/api/v2/process-city-data-in-bulk`

**Method**: `POST`

**Description**: Process weather data for a list of cities in bulk.

**Request Body**:
```json
{
  "process_id": 1
}
```

**Response**:
```json
{
  "message": "City data processing started."
}
```

### Get City Data Process

**Endpoint**: `/api/v1/get-city-data-process`

**Method**: `GET`

**Description**: Fetch the processed weather data for a specific process ID.

**Query Parameters**:
- `process_id` (int): The ID of the process to fetch data for.

**Response**:
```json
{
    "process_id": 1,
    "request_datetime": "2024-07-29 23:01:50",
    "total_cities": 167,
    "progress_percent": "35.93%",
    "process_id": 1,
    "results": [
        {
            "city_id": 3439525,
            "temperature": 6.15,
            "humidity": 59
        },
        {
            "city_id": 3439781,
            "temperature": 5.39,
            "humidity": 73
        },
        {
            "city_id": 3440645,
            "temperature": 7.13,
            "humidity": 73
        },
    ]
}
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.