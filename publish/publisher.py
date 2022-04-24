import time

import paho.mqtt.client as mqtt
import logging


class Publisher:
    def __init__(self, access):
        self.logger = logging.getLogger(__name__)

        self.mqttc = mqtt.Client()
        self.mqttc.username_pw_set(access, None)
        self.mqttc.connect("mqtt.thingsboard.cloud", 1883, 0)

        self.mqttc.loop_start()

    def send_message(self, message):
        infot = self.mqttc.publish('v1/devices/me/telemetry', message, 0)
        try:
            infot.wait_for_publish(2)
            self.logger.debug('Publish returned, rc = : ' + str(infot.rc))
            print('Publish returned, rc = : ' + str(infot.rc))
            return True  # We have not really checked if it worked
        except RuntimeError:
            self.logger.warning('Could not publish MQTT message - no internet.')
            print('Could not publish MQTT message - no internet.')
            return False

    def stop(self):
        self.mqttc.disconnect()

from Secrets import TEST_SECRET

if __name__ == '__main__':
    pub = Publisher(TEST_SECRET)
    big = 0

    while big < 100:
        big += 1
        message = {'Big': big, 'fat': 28, 'fake': 20}
        pub.send_message(str(message))
        time.sleep(5)

    pub.stop()
TEST_SECRET = 'VeQljVlS6kqmtj75e7ha'