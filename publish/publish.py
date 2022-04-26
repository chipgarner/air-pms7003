from Averager import DictAverager
import logging
import time


class Publish:
    def __init__(self, publisher_instance):
        self.logger = logging.getLogger(__name__)

        self.publisher = publisher_instance

        # This is to get the right dictionary keys stored in the averager.
        fake_data = {'1.0 ug/m3': 0, '2.5 ug/m3': 1, '10 ug/m3': 1, '0.3 n/dL': 0,
                     '0.5 n/dL': 0, '1.0 n/dL': 255, '2.5 n/dL': 255, '5.0 n/dL': 0,
                     '10 n/dL': 255, 'PM 10 EPA': 1, 'PM 2.5 EPA': 4}  # See test_pms7003.py
        self.dict_averager = DictAverager(fake_data, 11, self.publish_averaged_data)

        self.logger.info('MQTT publisher initialized.')

    def publish(self, data: dict):
        #  Don't publish all the data. Average N times and then publish.
        self.dict_averager.update(data)

    def publish_averaged_data(self, labelled, delta_t):
        self.logger.info('Delta t: ' + str(delta_t))
        time_stamped_results = {"ts": round(time.time() * 1000), "values": labelled}
        message = str(time_stamped_results)
        self.publisher.send_message(message)
        self.logger.debug(message)
