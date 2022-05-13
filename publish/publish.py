from Averager import DictAverager
import logging
import time


class Publish:
    def __init__(self, publisher_instance):
        self.logger = logging.getLogger(__name__)

        self.publisher = publisher_instance

        fake_data = None
        self.dict_averager = DictAverager(fake_data, 32, self.publish_averaged_data)

        self.logger.info('MQTT publisher initialized.')

    def publish(self, data: dict):
        #  Don't publish all the data. Average N times and then publish.
        self.dict_averager.update(data)

    def publish_averaged_data(self, labelled, delta_t):
        self.logger.info('Delta t: ' + str(delta_t))
        time_stamped_results = {"ts": round(time.time() * 1000), "values": labelled}
        message = str(time_stamped_results)
        self.publisher.send_message(message)
