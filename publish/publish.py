import logging
import time

from Averager import DictAverager


class Publish:
    def __init__(self, publisher_class):
        self.logger = logging.getLogger(__name__)

        self.publisher = publisher_class

        # This is to get the right dictionary keys stored in the averager.
        fake_data = {'1.0 ug/m3': 0, '2.5 ug/m3': 1, '10 ug/m3': 1, '0.3 n/dL': 0,
                     '0.5 n/dL': 0, '1.0 n/dL': 255, '2.5 n/dL': 255, '5.0 n/dL': 0,
                     '10 n/dL': 255, 'PM 10 EPA': 1, 'PM 2.5 EPA': 4}  # See test_pms7003.py
        self.dict_averager = DictAverager(fake_data, 11, self.publish_averaged_data)

        self.logger.info('MQTT publisher initialized.')

        self.saving_missed = False
        self.MISSED_CONN_FILE_NAME = 'data_not_sent.txt'

    def publish(self, data: dict):
        #  Don't publish all the data. Average N times and then publish.
        self.dict_averager.update(data)

    def publish_averaged_data(self, labelled, delta_t):
        time_stamped_results = {"ts": round(time.time() * 1000), "values": labelled}
        message = str(time_stamped_results)
        worked = self.publisher.send_message(message)

        if worked:
            if self.saving_missed:
                self.saving_missed = False
                self.send_missed_file()
        else:
            self.save_message(message)

        self.logger.info('Delta t: ' + str(delta_t))
        self.logger.debug(message)

    def save_message(self, message):
        if self.saving_missed:
            opener_type = "at"  # Appends to any existing data
        else:
            opener_type = "wt"  # Overwrites any existing data
            self.saving_missed = True

        with open(self.MISSED_CONN_FILE_NAME, opener_type) as a_file:
            a_file.write(message + '\n')

    def send_missed_file(self):
        with open(self.MISSED_CONN_FILE_NAME) as f:
            lines = f.readlines()

        self.logger.debug('Sending lines from file')
        self.publisher.send_message(lines)
        self.logger.debug(str(lines))
