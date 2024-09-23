import json
import logging
import logging.config
from pathlib import Path


def setup_logging() -> logging.Logger:
    # Create logs folder if not existed
    Path("logs").mkdir(exist_ok=True)

    # Load config and setup
    with open(Path("logging_setup", "config.json"), "r") as f:
        config = json.load(f)
        logging.config.dictConfig(config)
    logger = logging.getLogger("base")
    return logger


LOGGER = setup_logging()
