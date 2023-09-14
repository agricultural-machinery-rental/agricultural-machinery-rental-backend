import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = os.path.join(BASE_DIR, "../django.log")
REQUESTS_FILE = os.path.join(BASE_DIR, "../api_requests.log")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": LOG_FILE,
            "formatter": "main",
        },
        "request": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": REQUESTS_FILE,
            "formatter": "main",
        },
    },
    "formatters": {
        "main": {
            "format": " %(asctime)s, %(levelname)s,"
            " %(message)s, %(name)s, %(funcName)s,"
            " %(lineno)d,",
        },
        "simple": {
            "format": "%(log_color)s%(levelname)s,"
            " %(message)s, %(name)s, %(funcName)s,",
            "()": "colorlog.ColoredFormatter",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file", "request"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
