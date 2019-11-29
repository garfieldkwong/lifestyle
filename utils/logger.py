import logging, logging.handlers
import os
FORMAT = '%(asctime)s.%(msecs)03d|%(levelname)s| - %(message)s'
DATEFMT = '%Y-%m-%d %H:%M:%S'


def create_logger(log_name):
    """Create logger"""
    logger = logging.getLogger(log_name)

    directory = os.path.abspath(os.path.join('/', 'var', 'log', 'lifestyle'))
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    # Create rotate file logger
    file_handler = logging.handlers.RotatingFileHandler(
        os.path.join(directory, log_name),
        maxBytes=10*1024*1024,
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(FORMAT, DATEFMT))
    logger.addHandler(file_handler)

    # Create stream logger.
    console_log = logging.StreamHandler()
    console_log.setLevel(logging.DEBUG)
    console_log.setFormatter(logging.Formatter(FORMAT, DATEFMT))
    logger.addHandler(console_log)
    logger.setLevel(logging.INFO)
    return logger
