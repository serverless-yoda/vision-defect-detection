# common/logging.py

"""
Custom logging setup with correlation ID support for tracing logs across async operations.

This module provides:
- A `get_logger` function that returns a logger with a correlation ID filter.
- A `CorrelationIdContext` class to manage the current correlation ID.
- A `CorrelationIdFilter` class to inject the correlation ID into log records.
"""

import logging
import uuid

def get_logger(name: str):
    """
    Returns a logger instance with a correlation ID filter and stream handler.

    Args:
        name (str): The name of the logger, typically __name__.

    Returns:
        logging.Logger: Configured logger with correlation ID support.
    """
    logger = logging.getLogger(name)

    # Prevent adding multiple handlers if logger is reused
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] [CID:%(cid)s] %(message)s"
        )
        handler.setFormatter(formatter)
        handler.addFilter(CorrelationIdFilter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger

class CorrelationIdContext:
    """
    Manages the current correlation ID for logging context.
    Useful for tracing logs across asynchronous operations.
    """
    current_id = "N/A"

    @staticmethod
    def new_id() -> str:
        """
        Generates and sets a new UUID as the current correlation ID.

        Returns:
            str: The newly generated correlation ID.
        """
        CorrelationIdContext.current_id = str(uuid.uuid4())
        return CorrelationIdContext.current_id

class CorrelationIdFilter(logging.Filter):
    """
    Logging filter that injects the current correlation ID into log records.
    """

    def filter(self, record):
        """
        Adds the correlation ID to the log record.

        Args:
            record (logging.LogRecord): The log record being processed.

        Returns:
            bool: Always True to allow the log record to be processed.
        """
        record.cid = getattr(CorrelationIdContext, "current_id", "N/A")
        return True
