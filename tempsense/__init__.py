import time
from functools import partial

deg = u'\xb0'  # degree sign


def _output_to_temp(output):
    if output is not None:
        celsius = output
        fahrenheit = output * 9.0 / 5.0 + 32
        return celsius, fahrenheit
    else:
        print(f"Unable to read temperature for sensor")
        return None, None


def plain_prefix(names, pad=25):
    count = len(names)
    text = ("-" * 26 * count) + "\n"
    text += ("|".join([f'{names[i]}'.center(pad) for i in range(count)])) + "\n"
    return text


def plain(temps, hpad=12):
    count = len(temps)
    text = ("|".join([f'{deg}C'.center(hpad) + "|" + f'{deg}F'.center(hpad) for i in range(count)])) + "\n"
    formatted_temps = [f'{c:.3f}'.center(hpad) + "|" + f'{f:.3f}'.center(hpad) for (c, f) in temps]
    text += ("|".join(formatted_temps)) + "\n"
    return text


def csv(temps, sep=";"):
    formatted_temps = [f'{c:.3f}{sep}{f:.3f}' for (c, f) in temps]
    return (sep.join(formatted_temps)) + "\n"


def csv_prefix(names, sep=";"):
    count = len(names)
    text = (sep.join([f'{names[i]} {deg}C' + ";" + f'{names[i]} {deg}F' for i in range(count)])) + "\n"
    return text


def _out(path, text):
    if path is None:
        print(text)
    else:
        write(path, text)


def log_temp(snsr, interval=1, fmt="plain", path=None):
    out = partial(_out, path)
    try:
        formatter = plain if fmt == "plain" else csv
        prefixer = plain_prefix if fmt == "plain" else csv_prefix
        count = snsr.device_count()
        names = snsr.device_names()
        print('[press ctrl+c to end the script]')
        print('Reading temperature, number of sensors: {}'.format(count))

        out(prefixer(names))
        while True:
            temps = [_output_to_temp(snsr.temp(i)) for i in range(count)]
            text = formatter(temps)
            out(text)
            time.sleep(interval)

    # Scavenging work after the end of the program
    except KeyboardInterrupt:
        print('Script end!')


def write(path, text):
    with open(path, 'a') as f:
        f.write(text)
