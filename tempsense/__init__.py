import datetime
import time
from functools import partial

import pytz

from tempsense.logger import create_rotating_log

deg = u'\xb0'  # degree sign

DEFAULT_PAD = 25
DEFAULT_TZ = "UTC"


def get_timestamp(tz=DEFAULT_TZ):
    return pytz.timezone(tz).localize(datetime.datetime.utcnow()).isoformat()


def _output_to_temp(output, unit="c"):
    if output is not None:
        if unit == "c":  # celsius
            return output
        else:  # fahrenheit
            return output * 9.0 / 5.0 + 32
    else:
        print(f"Unable to read temperature for sensor")
        return None, None


def format_temp(t, pad=DEFAULT_PAD):
    if t is not None:
        return f'{t:.3f}'.center(pad)
    else:
        return ''.center(pad)


def plain_prefix(names, unit="c", pad=DEFAULT_PAD):
    count = len(names) + 1
    text = ["-" * (pad+1) * count]
    snsrs = [f'{names[i]} {deg}{unit.upper()}'.center(pad) for i in range(count - 1)]
    text += ["|".join(["time"] + snsrs)]
    return text


def plain(temps, tz=DEFAULT_TZ):
    timestamp = [get_timestamp(tz)]
    formatted_temps = [format_temp(t) for t in temps]
    return [("|".join(timestamp + formatted_temps))]


def csv(temps, tz=DEFAULT_TZ, sep=";"):
    timestamp = [get_timestamp(tz)]
    formatted_temps = [f'{format_temp(t,0)}' for t in temps]
    return [sep.join(timestamp + formatted_temps)]


def csv_prefix(names, unit="c", sep=";"):
    count = len(names)
    snsrs = [f'{names[i]} {deg}{unit.upper()}' for i in range(count)]
    text = [sep.join(["time"] + snsrs)]
    return text


def _out(log, text):
    if log is None:
        print(text)
    else:
        log.info(text)


def map_device_names(names, mapping):
    return [mapping[n] if n in mapping else n for n in names]


def log_temp(snsr, output=None, tz=DEFAULT_TZ, unit="c", fmt="plain", device_mapping=None,
             interval=1,
             log_rotate_interval=10,
             log_rotate_unit="s",
             log_backup_count=5
             ):
    if device_mapping is None:
        device_mapping = dict()
    try:
        formatter = plain if fmt == "plain" else csv
        prefixer = plain_prefix if fmt == "plain" else csv_prefix

        count = snsr.device_count()
        names = map_device_names(snsr.device_names(), device_mapping)

        if output is not None:
            log = create_rotating_log(
                output,
                lambda stream: stream.write("\n".join(prefixer(names, unit))+"\n"),
                when=log_rotate_unit,
                interval=log_rotate_interval,
                backupCount=log_backup_count
            )
        else:
            log = None
        out = partial(_out, log)

        print('[press ctrl+c to end the script]')
        print('Reading temperature, number of sensors: {}'.format(count))
        while True:
            temps = [_output_to_temp(snsr.temp(i), unit) for i in range(count)]
            text = "\n".join(formatter(temps, tz=tz))
            out(text)
            time.sleep(interval)

    # Scavenging work after the end of the program
    except KeyboardInterrupt:
        print('Script end!')
