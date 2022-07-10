import time
from typing import Optional

from tempsense import mqtt
from tempsense.mqtt import MQTTClient


def measure_temp(snsr,
                 unit="c",
                 device_mapping=None,
                 interval: int = 1,
                 log=None,
                 mqtt_client: Optional[MQTTClient] = None
                 ):
    if device_mapping is None:
        device_mapping = dict()
    try:
        count = snsr.device_count()
        names = map_device_names(snsr.device_names(), device_mapping)
        log.set_up(names)
        print('Press ctrl+c to end the script')
        print('Reading temperature, number of sensors: {}'.format(count))

        log.header()

        while True:
            temps = [snsr.temp(i) for i in range(count)]
            log.line(temps)
            if mqtt_client is not None:
                for t in temps:
                    if t.get_temp() is not None:
                        mqtt_client.send(map_device_name(t.device, device_mapping), t.get_temp(unit=unit))
                        # mqtt.pub(map_device_name(t.device, device_mapping), t.get_temp(unit=unit),
                        #         broker=mqtt_broker,
                        #         mqtt_auth={'username': mqtt_user, 'password': mqtt_password })
            time.sleep(interval)

    except KeyboardInterrupt:
        print('Exiting...')


def map_device_name(name, mapping):
    return mapping[name]


def map_device_names(names, mapping):
    return [map_device_name(n, mapping) if n in mapping else n for n in names]
