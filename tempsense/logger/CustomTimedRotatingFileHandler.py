from io import TextIOWrapper
from logging.handlers import TimedRotatingFileHandler


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):

    def __init__(self, filename, header_emitter, when='h', interval=1, backupCount=0,
                 encoding=None, delay=False, utc=False, atTime=None,
                 errors=None) -> None:
        self.header_emitter = header_emitter
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc, atTime, errors)

    def set_header_emitter(self, header_emitter):
        self.header_emitter = header_emitter

    def _open(self) -> TextIOWrapper:
        res = super()._open()
        self.header_emitter(res)
        return res
