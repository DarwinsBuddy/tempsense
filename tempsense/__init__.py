import time
from functools import partial

from tempsense.logger import create_rotating_log, get_format, DEFAULT_TZ, output_to_temp


def _out(log, text):
    if log is None:
        print(text)
    else:
        log.info(text)


def log_temp(snsr, output=None, tz=DEFAULT_TZ, unit="c", fmt="plain", device_mapping=None,
             interval=1,
             log_rotate_interval=10,
             log_rotate_unit="s",
             log_backup_count=5
             ):
    if device_mapping is None:
        device_mapping = dict()
    try:
        prefixer, formatter = get_format(fmt)

        count = snsr.device_count()
        names = map_device_names(snsr.device_names(), device_mapping)
        header = "\n".join(prefixer(names, unit))

        print('[press ctrl+c to end the script]')
        print('Reading temperature, number of sensors: {}'.format(count))

        if output is not None:
            log = create_rotating_log(
                output,
                lambda stream: stream.write(header+"\n"),
                when=log_rotate_unit,
                interval=log_rotate_interval,
                backupCount=log_backup_count
            )
        else:
            log = None
            print(header)
        out = partial(_out, log)

        while True:
            temps = [snsr.temp(i) for i in range(count)]
            text = "\n".join(formatter(temps, tz=tz))
            out(text)
            time.sleep(interval)

    # Scavenging work after the end of the program
    except KeyboardInterrupt:
        print('Script end!')


def map_device_names(names, mapping):
    return [mapping[n] if n in mapping else n for n in names]
