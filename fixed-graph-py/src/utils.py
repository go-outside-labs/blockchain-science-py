# -*- encoding: utf-8 -*-
# Util methods.

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv


def load_config() -> dict:
    """Load and set environment variables."""

    env_file = Path(".") / ".env"
    if not os.path.isfile(env_file):
        exit_with_error("Please create an .env file")

    env_vars = {}
    load_dotenv(env_file)

    try:
        set_logging(os.getenv("LOG_LEVEL"))
        return env_vars
    except KeyError as e:
        exit_with_error(f"Cannot extract env variables: {e}. Exiting.")


def set_logging(log_level: str) -> None:
    """Set logging level according to .env config."""

    if log_level == "INFO" or log_level == "info":
        logging.basicConfig(level=logging.INFO, format="%(message)s")

    elif log_level == "ERROR" or log_level == "error":
        logging.basicConfig(level=logging.ERROR, format="%(message)s")

    elif log_level == "DEBUG" or log_level == "debug":
        logging.basicConfig(level=logging.DEBUG, format="%(message)s")

    else:
        print(f"Logging level {log_level} is not available. Setting to ERROR")
        logging.basicConfig(level=logging.ERROR, format="%(message)s")


def log_error(string: str) -> None:
    """Print STDOUT error using the logging library."""

    logging.error("🚨 %s", string)


def log_info(string: str) -> None:
    """Print STDOUT info using the logging library."""

    logging.info("✅ %s", string)


def log_debug(string: str) -> None:
    """Print STDOUT debug using the logging library."""

    logging.debug("🟨 %s", string)


def exit_with_error(message: str) -> None:
    """Log an error message and halt the program."""

    log_error(message)
    sys.exit(1)
