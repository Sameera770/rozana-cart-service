"""
Local logging handlers for cart service.
Minimal subset of OMS handlers: file + stdout with JSON formatter.
"""
import logging
import os
from typing import Tuple

from app.logging.formatters import BaseJSONFormatter

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
LOG_DIR = os.getenv("LOG_DIR", os.path.join(BASE_DIR, "logs"))

# Ensure log directory exists on import (mirrors OMS behavior)
os.makedirs(LOG_DIR, exist_ok=True)


def get_local_file_handler(name: str) -> logging.Handler:
    formatter = BaseJSONFormatter()
    file_path = os.path.join(LOG_DIR, f"{name.replace('.', '_')}.log")
    handler = logging.FileHandler(file_path)
    handler.setFormatter(formatter)
    return handler


def get_stream_handler() -> logging.Handler:
    formatter = BaseJSONFormatter()
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    return handler


def get_handlers(name: str) -> Tuple[logging.Handler, logging.Handler]:
    """Return file + stream handlers (keeps API small)."""
    return get_local_file_handler(name), get_stream_handler()

