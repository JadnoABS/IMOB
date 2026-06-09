import logging
from pythonjsonlogger import jsonlogger

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    logHandler = logging.StreamHandler()

    formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s')
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)

    return logger
