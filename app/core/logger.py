import logging


class Logger:
    def __init__(
        self,
        name: str,
        level: int = logging.INFO,
        log_file: str = "data/system/app.log",
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Create console handler and set level
        ch = logging.StreamHandler()
        ch.setLevel(level)

        # Create file handler and set level
        fh = logging.FileHandler(log_file)
        fh.setLevel(level)

        # Create formatter and add it to the handlers
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

    def info(self, message: str):
        self.logger.info(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)


logger = Logger("Logger")
