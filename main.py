# main.py
from fastapi import FastAPI
from api.v1.vision_routes import router
from common.error_handlers import moderation_failed_handler
from domain.exceptions import ModerationFailedError

from api.middleware import CorrelationMiddleware, RequestLoggingMiddleware , RateLimitingMiddleware 

app = FastAPI(title="Azure Vision Defect Portal")

# Register middlewares
app.add_middleware(CorrelationMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimitingMiddleware, max_requests=5, window_seconds=30)  # optional usage

app.add_exception_handler(ModerationFailedError, moderation_failed_handler)
app.include_router(router, prefix="/api/v1")



# note: uvicorn main:app --reload --port 8000