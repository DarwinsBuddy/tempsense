import time
from typing import Optional

from tempsense import mqtt
from tempsense.mqtt import MQTTClient


def measure_temp(snsr,
                 unit="c",
                 interval: int = 1,
                 log=None,
                 mqtt_client: Optional[MQTTClient] = None
                 ):
    try:
        count = snsr.device_count()
        names = snsr.device_names()
        if log is not None:
            log.set_up(names)
        print('Press ctrl+c to end the script')
        print('Reading temperature from {} sensors'.format(count))

        if log is not None:
            log.header()

        while True:
            temps = [snsr.temp(i) for i in range(count)]
            if log is not None:
                log.line(temps)
            if mqtt_client is not None:
                mqtt_client.pub(temps, unit=unit)
            time.sleep(interval)

    except KeyboardInterrupt:
        if mqtt_client is not None:
            mqtt_client.close()
        print('Exiting...')

