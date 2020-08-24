# logger.py
import logging


class Logger:
    def __init__(self, name):
        # create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(ch)

    @property
    def l(self):  # noqa: E743
        return self.logger

    def logger(self, logger):
        self.logger = logger
