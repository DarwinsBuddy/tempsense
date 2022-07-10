import logging
from tempsense.logger.CustomTimedRotatingFileHandler import CustomTimedRotatingFileHandler


def create_rotating_log(path, header_emitter):
    """
    Creates a rotating log
    """
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)

    # add a rotating handler
    handler = CustomTimedRotatingFileHandler(path, header_emitter, when="s", interval=10, backupCount=5)
    logger.addHandler(handler)

    return logger
