# common/error_handlers.py

"""
Custom error handlers and middleware for FastAPI application.

Includes:
- A handler for VisionAnalysisError exceptions.
- Middleware to inject and propagate correlation IDs for request tracing.
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from common.logging import CorrelationIdContext, get_logger
from domain.exceptions import VisionAnalysisError
from starlette.middleware.base import BaseHTTPMiddleware

logger = get_logger(__name__)

async def vision_defect_failed_handler(request: Request, exc: VisionAnalysisError):
    """
    Handles VisionAnalysisError exceptions and returns a structured JSON response.

    Args:
        request (Request): The incoming FastAPI request.
        exc (VisionAnalysisError): The exception instance raised during vision analysis.

    Returns:
        JSONResponse: A 500 error response with error details.
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Azure Vision Defect Detection system failed",
            "details": str(exc)
        }
    )

class CorrelationMiddleware(BaseHTTPMiddleware):
    """
    Middleware to generate and attach a correlation ID to each request.

    The correlation ID is stored in request.state and added to the response headers
    for traceability across logs and services.
    """

    async def dispatch(self, request: Request, call_next):
        # Generate a new correlation ID for the request
        cid = CorrelationIdContext.new_id()

        # Attach it to the request state for downstream access
        request.state.correlation_id = cid

        # Process the request and attach the correlation ID to the response headers
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = cid
        return response
