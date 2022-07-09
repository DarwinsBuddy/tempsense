import argparse

from tempsense import log_temp

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--interval", type=int, default=1, help="read interval in sec")
ap.add_argument("-f", "--format", choices=['csv', 'plain'], help="Output format", default="plain")
ap.add_argument("-o", "--output", type=str, help="Output path", default=None)
ap.add_argument("-m", "--mock", action='store_true', help="Mock temperatures", default=False)
args = vars(ap.parse_args())


def usage_and_exit():
    print(ap.format_help())
    exit(1)


if __name__ == '__main__':
    if args.get('mock'):
        from .test.sensor import MockedDS18B20 as DS18B20
    else:
        from sensor import DS18B20
    log_temp(DS18B20(), fmt=args.get("format"), path=args.get("output"))
