import argparse
import json

from tempsense import log_temp

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--interval", type=int, default=1, help="read interval in sec")
ap.add_argument("-f", "--format", choices=['csv', 'plain'], help="Output format", default="plain")
ap.add_argument("-o", "--output", type=str, help="Output path", default=None)
ap.add_argument("-m", "--mock", action='store_true', help="Mock temperatures", default=False)
ap.add_argument("-u", "--unit", choices=['c', 'f'], help="Temperature unit (c: Celsius, f: Fahrenheit)", default='c')
ap.add_argument("-tz", "--timezone", type=str, help="Timezone (e.g. 'utc', 'Europe/Vienna')", default='utc')
ap.add_argument("-d", "--devices", type=argparse.FileType('r', encoding='UTF-8'),
                help="Path to json containing map for sensor name to human readable name", default=None)
args = vars(ap.parse_args())


def usage_and_exit():
    print(ap.format_help())
    exit(1)


if __name__ == '__main__':
    if args.get('mock'):
        from .test.sensor import MockedDS18B20 as DS18B20
    else:
        from .sensor import DS18B20

    if args.get("devices") is not None:
        dmap = json.load(args.get("devices"))
    else:
        dmap = {}
    log_temp(DS18B20(),
             tz=args.get("timezone"),
             interval=args.get("interval"),
             unit=args.get("unit"),
             fmt=args.get("format"),
             path=args.get("output"),
             device_mapping=dmap
     )
