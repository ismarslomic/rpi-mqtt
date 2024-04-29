#!/usr/bin/env python3
"""Timer running a function in a separate thread"""
import logging
import threading
from collections.abc import Callable


class RepeatTimer(threading.Timer):
    """Timer running a function in a separate thread"""

    _logger: logging.Logger

    def __init__(self, name: str, interval: float, function: Callable):
        super().__init__(interval=interval, function=function)
        logger_name: str = f"{__name__}.{name}"
        self._logger = logging.getLogger(logger_name)

    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
            self._logger.info("Executed function")

    def start(self):
        super().start()
        self._logger.debug("Started timer")

    def cancel(self):
        super().cancel()
        self._logger.debug("Cancelled timer")
