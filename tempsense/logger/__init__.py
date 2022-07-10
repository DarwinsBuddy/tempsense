import datetime
import logging

import pytz

from tempsense.logger.CustomTimedRotatingFileHandler import CustomTimedRotatingFileHandler
from tempsense.sensor import SensorData

deg = u'\xb0'  # degree sign


def get_format(fmt):
    if fmt == 'plain':
        formatter = plain
        prefixer = plain_header
    elif fmt == 'csv':
        formatter = csv
        prefixer = csv_header
    else:
        formatter = lambda x: x
        prefixer = lambda x: x

    return prefixer, formatter


def create_rotating_log(path, header_emitter, **kwargs):
    """
    Creates a rotating log
    """
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)

    # add a rotating handler
    handler = CustomTimedRotatingFileHandler(path, header_emitter, **kwargs)
    logger.addHandler(handler)

    return logger


DEFAULT_PAD = 25
DEFAULT_TZ = "UTC"


def get_timestamp(tz=DEFAULT_TZ):
    return pytz.timezone(tz).localize(datetime.datetime.utcnow()).isoformat()


def output_to_temp(output, unit="c"):
    if output is not None:
        if unit == "c":  # celsius
            return output
        else:  # fahrenheit
            return output * 9.0 / 5.0 + 32
    else:
        print(f"Unable to read temperature for sensor")
        return None


def plain_header(names, unit="c", pad=DEFAULT_PAD):
    count = len(names)
    time_pad = 34
    text = ["-" * ((time_pad + 1) + ((pad + 1) * count))]
    snsrs = [f'{names[i]} {deg}{unit.upper()}'.center(pad) for i in range(count)]
    text += ["|".join(["time".center(time_pad)] + snsrs)]
    return text


def plain(sensor_data_list: [SensorData], unit='c', tz=DEFAULT_TZ):
    timestamp = [get_timestamp(tz).center(34)]
    formatted_temps = [data.format_temp(unit).center(DEFAULT_PAD) for data in sensor_data_list]
    return [("|".join(timestamp + formatted_temps))]


def csv(sensor_data_list, unit='c', tz=DEFAULT_TZ, sep=";"):
    timestamp = [get_timestamp(tz)]
    formatted_temps = [data.format_temp(unit) for data in sensor_data_list]
    return [sep.join(timestamp + formatted_temps)]


def csv_header(names, unit="c", sep=";"):
    count = len(names)
    snsrs = [f'{names[i]} {deg}{unit.upper()}' for i in range(count)]
    text = [sep.join(["time"] + snsrs)]
    return text
