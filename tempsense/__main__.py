import argparse
import json

from tempsense import log_temp

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--interval", type=int, default=10, help="read interval in sec")
ap.add_argument("-f", "--format", choices=['csv', 'plain'], help="Output format", default="plain")
ap.add_argument("-o", "--output", type=str, help="Output path", default=None)
ap.add_argument("-m", "--mock", action='store_true', help="Mock temperatures", default=False)
ap.add_argument("-u", "--unit", choices=['c', 'f'], help="Temperature unit (c: Celsius, f: Fahrenheit)", default='c')
ap.add_argument("-tz", "--timezone", type=str, help="Timezone (e.g. 'utc', 'Europe/Vienna')", default='utc')
ap.add_argument("-d", "--devices", type=argparse.FileType('r', encoding='UTF-8'),
                help="Path to json containing map for sensor name to human readable name", default=None)
ap.add_argument("-rb", "--rotate_backup", type=int, default=7, help="log backup count (default: 7)")
ap.add_argument("-ri", "--rotate_interval", type=int, default=1,
                help="rotate interval in [ru] units (default: 1)")
ap.add_argument("-ru", "--rotate_unit", choices=['s', 'm', 'h', 'd', 'midnight'], default='d',
                help="""
                    log rotate interval unit
                    s: sec
                    m: minutes
                    h: hours
                    d: days
                    midnight: once a day interval ignored
                    """)

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
             output=args.get("output"),
             device_mapping=dmap,
             log_rotate_interval=args.get("rotate_interval"),
             log_rotate_unit=args.get("rotate_unit"),
             log_backup_count=args.get("rotate_backup")
             )
