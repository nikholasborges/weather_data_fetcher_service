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

## Installation

### Clone the Repository

```sh
git clone https://github.com/nikholasborges/weather-data-fetcher-service.git
cd weather-data-fetcher-service
```

### Configure the enviroment

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

To run the application locally, fist you need to run the redis docker container:

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

To build and run the Docker container, execute the code below, this will execute the redis container and the service container:

```sh
docker-compose up --build
```

To run the containers in detached mode:

```sh
docker-compose up --build -d
```

### Stop Docker Containers

To stop the Docker containers (if in detached mode):

```sh
docker-compose down
```

## Makefile Targets

The `Makefile` includes several targets to streamline common tasks:

- `make install`: Install dependencies using Poetry.
- `make run`: Run the application.
- `make dev`: Run the application in development mode.
- `make lint`: Lint the code using flake8.
- `make test`: Run tests using pytest and generate a coverage report.
- `make clean`: Clean up the project directory.
- `make build-docker`: Build the Docker image.
- `make run-docker`: Run the Docker container.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
```