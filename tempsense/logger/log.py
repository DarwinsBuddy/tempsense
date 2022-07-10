import datetime
import logging

import pytz

from tempsense.logger.CustomTimedRotatingFileHandler import CustomTimedRotatingFileHandler
from tempsense.sensor import SensorData

deg = u'\xb0'  # degree sign
DEFAULT_TZ = "UTC"


class Log:

    def __init__(self,
                 path=None,
                 log_rotate_interval: int = 10,
                 log_rotate_unit: str = "s",
                 log_backup_count: int = 5,
                 fmt="plain",
                 unit="c",
                 tz=DEFAULT_TZ
                 ):
        """
        Creates a rotating log
        """
        self.fmt = fmt
        self.tz = tz
        self.unit = unit
        self.log_rotate_unit = log_rotate_unit
        self.log_backup_count = log_backup_count
        self.path = path
        self.log_rotate_interval = log_rotate_interval
        self.logger = logging.getLogger("Rotating Log")
        self.logger.setLevel(logging.INFO)
        self.sensor_names = None
        self.handler = None
        self.initialized = False

        if self.fmt == 'plain':
            self.pad = 25
            self.time_pad = 34
            self.sep = "|"
        elif self.fmt == 'csv':
            self.sep = ";"
            self.pad = 0
            self.time_pad = 0
        else:
            raise Exception(f"Unsupported format {fmt}")

    def set_up(self, sensor_names):
        self.sensor_names = sensor_names
        if self.path is not None:
            if self.initialized:
                self.logger.removeHandler(self.handler)
                self.initialized = False

            self.handler = CustomTimedRotatingFileHandler(
                self.path,
                header_emitter=lambda stream: stream.write(self._header()+"\n"),
                when=self.log_rotate_unit,
                interval=self.log_rotate_interval,
                backupCount=self.log_backup_count
            )
            self.logger.addHandler(self.handler)
        self.initialized = True

    def get_timestamp(self):
        return pytz.timezone(self.tz).localize(datetime.datetime.utcnow()).isoformat()

    def header(self):
        if self.path is None:
            print(self._header())
        else:
            pass  # done implicitly on creating of rotating file log

    def line(self, sensor_data_list: [SensorData]):
        line = self._line(sensor_data_list)
        if self.path is None:
            print(line)
        else:
            self.logger.info(line)

    def _header(self):
        count = len(self.sensor_names)
        snsrs = [f'{self.sensor_names[i]} {deg}{self.unit.upper()}'.center(self.pad) for i in range(count)]
        text = self.sep.join(["time".center(self.time_pad)] + snsrs)
        return text

    def _line(self, sensor_data_list: [SensorData]):
        timestamp = [self.get_timestamp().center(self.time_pad)]
        formatted_temps = [data.format_temp(self.unit).center(self.pad) for data in sensor_data_list]
        return self.sep.join(timestamp + formatted_temps)
