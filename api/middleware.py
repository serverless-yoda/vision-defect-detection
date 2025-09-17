# api/middleware.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from common.logging import CorrelationIdContext, get_logger
from collections import defaultdict
from fastapi import HTTPException
import time


logger = get_logger(__name__)


class RateLimitingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests=10, window_seconds=60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        request_times = self.requests[client_ip]

        # Purge requests outside the window
        self.requests[client_ip] = [t for t in request_times if t > current_time - self.window_seconds]

        if len(self.requests[client_ip]) >= self.max_requests:
            raise HTTPException(status_code=429, detail="Too many requests")

        self.requests[client_ip].append(current_time)
        return await call_next(request)


class CorrelationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = CorrelationIdContext.new_id()
        logger.info(f"CorrelationMiddleware: Assigned ID {correlation_id} to request")
        request.state.correlation_id = correlation_id
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = (time.perf_counter() - start_time) * 1000
        logger.info(f"{request.method} {request.url.path} completed in {process_time:.2f} ms")
        return response