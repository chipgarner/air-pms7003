from publish.publisher import Publisher
from Secrets import SECRET  # Credential string for MQTT on Thingsboard - don't put credentials in Git
from Averager import DictAverager
import logging


class Publish:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.publisher = Publisher(SECRET)

        # This is to get the right dictionary keys stored in the averager.
        fake_data = {'1.0 ug/m3': 0, '2.5 ug/m3': 1, '10 ug/m3': 1, '0.3 n/dL': 0,
                     '0.5 n/dL': 0, '1.0 n/dL': 255, '2.5 n/dL': 255, '5.0 n/dL': 0,
                     '10 n/dL': 255, 'PM 10 EPA': 1, 'PM 2.5 EPA': 4}  # See test_pms7003.py
        self.dict_averager = DictAverager(fake_data, 11, self.call_on_count)

        self.logger.info('MQTT publisher initialized.')

    def publish(self, data: dict):
        self.dict_averager.update(data)

    def call_on_count(self, labelled, delta_t):
        self.logger.info('Delta t: ' + str(delta_t))
        message = str(labelled)
        self.publisher.send_message(message)
        self.logger.debug(message)
