import logging
from app.logging.handlers import get_handlers


def get_app_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.handlers.clear()
        file_handler, stream_handler = get_handlers(name)
        for handler in (file_handler, stream_handler):
            logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger
