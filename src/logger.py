import logging

from path_vars import LOG_FILE


class Logger:
    def __init__(self) -> None:
        self.file_name = LOG_FILE
        self.file_mode = "a"
        self.format = "%(asctime)s - %(message)s"
        self.basic_conf()

    def basic_conf(self) -> None:
        logging.basicConfig(
            filename=self.file_name, filemode=self.file_mode, format=self.format
        )

    def log_error(self, msg: str) -> None:
        logging.error(msg)
