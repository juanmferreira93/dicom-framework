import logging

from decouple import config


class Logger:
    def __init__(self):
        self.levels = ["info", "error"]
        self.logger = logging.getLogger("DICOM-Logger")

    def log(self, level, message):
        if config("ENV") == "development":
            logging.basicConfig(
                filename="development.log", filemode="w", level=logging.DEBUG
            )
            self.logger.warning(message)
        else:
            if level in self.levels:
                logging.basicConfig(
                    filename="production.log", filemode="w", level=logging.INFO
                )
                eval(f"self.logger.{level}('{message}')")
