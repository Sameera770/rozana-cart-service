"""
Lightweight JSON formatter for cart service logs (mirrors OMS style).
"""
import json
import logging
import os
from datetime import datetime

APPLICATION_ENVIRONMENT = os.getenv("APPLICATION_ENVIRONMENT", "local")


class BaseJSONFormatter(logging.Formatter):
    """Basic JSON formatter used by local handlers."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line_number": record.lineno,
            "environment": APPLICATION_ENVIRONMENT,
            "service": "rozana-cart",
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False, default=str)

