import time
import paho.mqtt.client as mqtt
import logging
import check_internet


class Publisher:
    def __init__(self, access):
        self.logger = logging.getLogger(__name__)

        self.last_publish_time = time.time()

        self.mqttc = mqtt.Client(client_id=self.getserial(), clean_session=False)
        self.mqttc.on_publish = self.on_publish

        #  Queued messages, e.g. while there is no internet, will collect and be sent to the broker
        #  quickly. Most brokers limit incoming messages, e.g. 20 per second.
        MAX_QUEUED_MESSAGES = 20
        self.mqttc.max_queued_messages_set(MAX_QUEUED_MESSAGES)

        self.mqttc.enable_logger(self.logger)
        self.mqttc.username_pw_set(access, None)
        try:
            self.mqttc.connect("mqtt.thingsboard.cloud", 1883, 0)
        except Exception as ex:
            self.logger.error('Publisher could not connect. ' + str(ex))

        self.mqttc.loop_start()

    def getserial(self):
    # Extract Rapberry Pi serial number from cpuinfo file
        cpuserial = "0000000000001234"
        try:
            f = open('/proc/cpuinfo','r')
            for line in f:
                if line[0:6]=='Serial':
                    cpuserial = line[10:26]
            f.close()
        except:
            cpuserial = "ERROR000000000"

        self.logger.info('Serial number: ' + cpuserial)

        return cpuserial

    def send_message(self, a_message):
        last_success_interval = time.time() - self.last_publish_time
        if last_success_interval < 200000000:
            return self.publish(a_message)

        else:
            self.logger.info('Not publishing, no internet?')
            self.logger.debug('Not for ' + str(int(last_success_interval)) + ' seconds')
            return False

    def publish(self, a_message):
        infot = self.mqttc.publish('v1/devices/me/telemetry', a_message, qos=1)
        self.logger.debug('Paho info before =: ' + str(infot))
        if infot.rc == mqtt.MQTT_ERR_QUEUE_SIZE:
            mqtt_connected = self.mqttc.is_connected()
            internet = check_internet.check_internet_connection()
            self.logger.debug('Connected: ' + str(mqtt_connected) + ' Internet: ' +str(internet))
            if internet:
                self.mqttc.reconnect()
            return False
        else:

            try:
                infot.wait_for_publish(2)
                self.logger.debug('Paho info =: ' + str(infot))
                if infot.rc != 0: # Debugging
                    self.logger.error('mqttc publish returned rc = ' + str(infot.rc))

                return True  # We have not really checked if it worked
            except RuntimeError:  # This is very intermittent
                self.logger.warning('Could not publish MQTT message.')
                return False
            except ValueError as ex:
                self.logger.warning(str(ex))
                if "ERR_QUEUE_SIZE" in str(ex):
                    if not self.mqttc.is_connected() and check_internet.check_internet_connection():
                        self.mqttc.reconnect()
                    return False
                else:
                    raise(ex)

    def on_publish(self, client, data, message_id):
        self.logger.debug('Published, id = ' + str(message_id))
        self.last_publish_time = time.time()

    def stop(self):
        self.mqttc.disconnect()
