from structlog import PrintLogger


class Logger:
    def __init__(self):
        self.logger = PrintLogger()

    def info(self, info_message):
        self.logger.info(info_message)

    def debug(self, debug_message):
        self.logger.debug(debug_message)
