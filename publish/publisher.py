import paho.mqtt.client as mqtt
import logging


class Publisher:
    def __init__(self, access):
        self.logger = logging.getLogger(__name__)

        self.mqttc = mqtt.Client()
        self.mqttc.username_pw_set(access, None)
        self.mqttc.connect("mqtt.thingsboard.cloud", 1883, 60)

        self.mqttc.loop_start()

    def send_message(self, message):
        infot = self.mqttc.publish('v1/devices/me/telemetry', message, 0)
        try:
            infot.wait_for_publish()
        except RuntimeError:
            self.logger.exception('Could not publish MQTT message - no internet?')

    def stop(self):
        self.mqttc.disconnect()
