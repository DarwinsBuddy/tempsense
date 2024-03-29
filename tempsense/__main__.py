import configargparse
import json

from tempsense import measure_temp
from tempsense.logger.log import Log

ap = configargparse.ArgumentParser()
ap.add_argument("-c", "--config", is_config_file=True, help="path to config")
ap.add_argument("-q", "--quiet", action='store_true', help="No logs, no output (overrides all log related options)")
ap.add_argument("-i", "--interval", type=int, default=10, help="read interval in sec")
ap.add_argument("-f", "--format", choices=['csv', 'plain'], help="Output format", default="plain")
ap.add_argument("-o", "--output", type=str, help="Output path", default=None)
ap.add_argument("-m", "--mock", action='store_true', help="Mock temperatures", default=False)
ap.add_argument("-mqtt", "--mqtt_broker", type=str, help="MQTT Broker address", default=None)
ap.add_argument("-user", "--mqtt_user", type=str, help="MQTT user", default=None)
ap.add_argument("-pw", "--mqtt_password", type=str, help="MQTT password", default=None)
ap.add_argument("-topic", "--mqtt_topic_prefix", type=str, help="MQTT topic_prefix", default='home-assistant/ds18b20')
ap.add_argument("-u", "--unit", choices=['c', 'f'], help="Temperature unit (c: Celsius, f: Fahrenheit)", default='c')
ap.add_argument("-dp", "--decimal_places", type=int, help="Precision in decimal places", default=0)
ap.add_argument("-tz", "--timezone", type=str, help="Timezone (e.g. 'utc', 'Europe/Vienna')", default='utc')
ap.add_argument("-d", "--device_map", type=configargparse.FileType('r', encoding='UTF-8'),
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

    if args.get("device_map") is not None:
        dmap = json.load(args.get("device_map"))
    else:
        dmap = {}

    if args.get('mqtt_broker') is not None:
        from tempsense.mqtt import MQTTClient
        mqtt_client = MQTTClient(
            broker=args.get('mqtt_broker'),
            topic_prefix=args.get("mqtt_topic_prefix"),
            mqtt_auth={
                "username": args.get('mqtt_user'),
                "password": args.get('mqtt_password')
            }
        )
    else:
        mqtt_client = None
    if args.get("quiet"):
        log = None
    else:
        log = Log(
            args.get("output"),
            fmt=args.get("format"),
            unit=args.get("unit"),
            decimal_places=args.get('decimal_places'),
            log_rotate_interval=args.get("rotate_interval"),
            log_rotate_unit=args.get("rotate_unit"),
            log_backup_count=args.get("rotate_backup"),
            tz=args.get("timezone")
        )
    measure_temp(DS18B20(dmap),
                 interval=args.get("interval"),
                 log=log,
                 mqtt_client=mqtt_client
                 )
