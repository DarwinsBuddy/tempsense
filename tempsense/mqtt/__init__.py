import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish


class MQTTClient:
    def __init__(self, broker='127.0.0.1', mqtt_auth=None):
        self.broker = broker
        self.mqtt_auth = mqtt_auth
        self.client = mqtt.Client("ha-client")
        self.client.username_pw_set(**mqtt_auth)
        self.connect()

    def connect(self):
        self.client.connect(self.broker)
        self.client.loop_start()

    def send(self, sensor_name, value, topic_prefix='home-assistant/ds18b20'):
        try:
            self.client.publish(f'{topic_prefix}/{sensor_name}', value)
        except Exception as e:
            print("ERROR - Unable to send MQTT msg", e)
            self.client.loop_stop(force=True)
            self.client.disconnect()
            self.connect()

    def close(self):
        self.client.disconnect()


def pub(sensor_name, value, topic_prefix='home-assistant/ds18b20', broker='127.0.0.1', mqtt_auth=None):
    try:
        publish.single(f'{topic_prefix}/{sensor_name}', value, hostname=broker, auth=mqtt_auth)
    except Exception as e:
        print("ERROR - Unable to send MQTT msg", e)
