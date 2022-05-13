import save.saver
import logging
from Averager import DictAverager
import time


class Save:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.saver = save.saver.Saver()

        fake_data = None
        self.dict_averager = DictAverager(fake_data, 11, self.save_averaged_data)

        self.logger.info('Data file saver initialized.')

    def save(self, data: dict):
        #  Don't publish all the data. Average N times and then publish.
        self.dict_averager.update(data)

    def save_averaged_data(self, labelled, delta_t):
        self.logger.info('Delta t: ' + str(delta_t))
        time_stamped_results = {"ts": round(time.time() * 1000), "values": labelled}
        message = str(time_stamped_results)
        self.saver.save_line(message)
