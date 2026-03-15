import logging
from os import makedirs
from os.path import dirname

def make_logger(path: str, name: str) -> logging.Logger:
    makedirs(dirname(path), exist_ok=True) # creates all parent directories if they don't exist

    logger = logging.getLogger(name)

    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s')
    fileHandler = logging.FileHandler(path, 'a')
    fileHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)

    return logger