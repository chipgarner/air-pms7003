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
        #  Don't save all the data. Average N times and then save.
        self.dict_averager.update(data)

    def save_averaged_data(self, labelled, _):
        now = {"time": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}
        time_stamped_results = now.update(labelled)
        # message = str(time_stamped_results)
        self.saver.save_line(time_stamped_results)
