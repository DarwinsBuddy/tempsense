import time

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish


DEFAULT_TOPIC_PREFIX = 'home-assistant/ds18b20'


class MQTTClient:
    def __init__(self, broker='127.0.0.1', mqtt_auth=None, topic_prefix=DEFAULT_TOPIC_PREFIX):
        self.topic_prefix = topic_prefix
        self.broker = broker
        self.mqtt_auth = mqtt_auth
        self.client = mqtt.Client("ha-client")
        self.client.username_pw_set(**mqtt_auth)
        self.connect()

    def connect(self):
        self.client.connect(self.broker)
        self.client.loop_start()

    def send(self, topic, value):
        try:
            self.client.publish(f'{self.topic_prefix}/{topic}', value)
        except Exception as e:
            print("ERROR - Unable to send MQTT msg", e)
            self.client.loop_stop(force=True)
            self.client.disconnect()
            self.connect()

    def pub(self, temps, unit="c"):
        self.send("availability", "online")
        for t in temps:
            if t.get_temp() is not None:
                self.send(t.device, t.get_temp(unit=unit))

    def close(self):
        self.send("availability", "offline")
        time.sleep(1)
        self.client.disconnect()


def pub(sensor_name, value, topic_prefix=DEFAULT_TOPIC_PREFIX, broker='127.0.0.1', mqtt_auth=None):
    try:
        publish.single(f'{topic_prefix}/{sensor_name}', value, hostname=broker, auth=mqtt_auth)
    except Exception as e:
        print("ERROR - Unable to send MQTT msg", e)
