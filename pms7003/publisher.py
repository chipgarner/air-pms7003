import paho.mqtt.client as mqtt


class Publisher:
    def __init__(self):
        self.mqttc = mqtt.Client()
        self.mqttc.username_pw_set('GcV2Ha20W1QlylGAmACF', None)
        # PiAir1 GPHs4tBNYCbLSOHeS6Nm
        # piAir2 yMGrQJPJqDSbuO3BHm546
        self.mqttc.connect("192.168.1.191", 1883, 60)

        self.mqttc.loop_start()

    def send_message(self, message):
        infot = self.mqttc.publish('v1/devices/me/telemetry', message, 0)
        infot.wait_for_publish()

    def stop(self):
        self.mqttc.disconnect()
