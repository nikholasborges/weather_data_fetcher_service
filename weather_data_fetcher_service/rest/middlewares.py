import asyncio
from async_timeout import timeout
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class TimeoutMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, timeout_seconds: int):
        super().__init__(app)
        self.timeout_seconds = timeout_seconds

    async def dispatch(self, request: Request, call_next):
        try:
            async with timeout(self.timeout_seconds):
                response = await call_next(request)
            return response
        except asyncio.TimeoutError:
            raise HTTPException(status_code=408, detail="Request timeout")
