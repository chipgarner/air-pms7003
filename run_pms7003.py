import logging
import logging.handlers
import os
import time

from sense.sensors import PmsSensor

try:
    from display.display import Display
    display = True
except ModuleNotFoundError:
    display = False  # Assuming this means no display is installed
from publish.publish import Publish


class RunMePms7003:
    def __init__(self):
        format = '%(asctime)s %(name)s %(message)s'
        logging.basicConfig(format=format,
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.INFO)
        self.logger = logging.getLogger()

        directory_path = os.path.dirname(__file__)
        file_path = directory_path + '/info.log'
        formatter = logging.Formatter(format, datefmt='%m/%d/%Y %I:%M:%S %p')
        log_handler = logging.handlers.TimedRotatingFileHandler(file_path, when='D', interval=1,
                                                                backupCount=5, utc=True)
        file_path = directory_path + '/warning.log'
        log_handler.setLevel(logging.INFO)
        log_handler.setFormatter(formatter)
        self.logger.addHandler(log_handler)

        warning_log_handler = logging.handlers.TimedRotatingFileHandler(file_path, when='D', interval=1,
                                                                        backupCount=5, utc=True)
        warning_log_handler.setLevel(logging.WARNING)
        warning_log_handler.setFormatter(formatter)
        self.logger.addHandler(warning_log_handler)

        self.sensors = PmsSensor()

        if display:
            self.display = Display()
        else:
            self.logger.warning('Could not import display, assuming there is none.')
            self.display = None

        self.publish = Publish()

        self.running = True

    def loop(self):
        self.logger.info('Starting loop')
        while self.running:
            latest = self.sensors.get_latest()
            if self.display is not None:
                self.display.display(latest)
            time_stamped_latest = {"ts": round(time.time() * 1000), "values": latest}
            print(time_stamped_latest)
            self.publish.publish(time_stamped_latest)

        self.logger.error('Exited main loop')
        self.sensors.stop()


if __name__ == '__main__':
    runner = RunMePms7003()
    runner.loop()
