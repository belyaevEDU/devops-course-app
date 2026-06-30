import logging

def make_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s')
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    logger.addHandler(streamHandler)

    return logger
