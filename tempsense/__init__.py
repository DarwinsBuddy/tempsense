import datetime
import time
from functools import partial

import pytz

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


def _out(path, lines):
    if path is None:
        print("\n".join(lines))
    else:
        write(path, "\n".join(lines))


def map_device_names(names, mapping):
    return [mapping[n] if n in mapping else n for n in names]


def log_temp(snsr, tz=DEFAULT_TZ, unit="c", interval=1, fmt="plain", path=None, device_mapping=None):
    if device_mapping is None:
        device_mapping = dict()
    out = partial(_out, path)
    try:
        formatter = plain if fmt == "plain" else csv
        prefixer = plain_prefix if fmt == "plain" else csv_prefix
        count = snsr.device_count()
        names = map_device_names(snsr.device_names(), device_mapping)
        print('[press ctrl+c to end the script]')
        print('Reading temperature, number of sensors: {}'.format(count))
        out(prefixer(names, unit))
        while True:
            temps = [_output_to_temp(snsr.temp(i), unit) for i in range(count)]
            text = formatter(temps, tz=tz)
            out(text)
            time.sleep(interval)

    # Scavenging work after the end of the program
    except KeyboardInterrupt:
        print('Script end!')


def write(path, text):
    with open(path, 'a') as f:
        f.write(text)
