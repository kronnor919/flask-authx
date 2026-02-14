import logging
import logging.handlers
from flask_authx._interfaces.service import ILoggerService
from pathlib import Path


class LocalFileLoggerService(ILoggerService):
    def __init__(self, filepath: str) -> None:
        self._filepath = filepath

        try:
            Path(self._filepath).touch(exist_ok=True)

        except FileNotFoundError:
            raise FileNotFoundError("Some parent folders doesn't exist.")

        self._logger_name = "local-file-logger"
        self._logger = logging.getLogger(self._logger_name)
        self._formatter = logging.Formatter(
            "[%(levelname)s] %(message)s. At %(asctime)s", "%d-%m-%Y %H:%M:%S"
        )
        self._handler = logging.handlers.TimedRotatingFileHandler(
            self._filepath, "midnight", 1, 7, "utf-8"
        )
        self._handler.setLevel(logging.DEBUG)
        self._handler.setFormatter(self._formatter)

    def debug(self, message: str) -> str:
        self._logger.debug(message)
        return message

    def info(self, message: str) -> str:
        self._logger.info(message)
        return message

    def warn(self, message: str = "Empty log") -> str:
        self._logger.warning(message)
        return message

    def error(self, message: str) -> str:
        self._logger.error(message)
        return message

    def fatal(self, message: str) -> str:
        self._logger.critical(message)
        return message
