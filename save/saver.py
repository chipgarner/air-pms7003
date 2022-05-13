import logging
import os
import time


MAX_LINES_IN_FILE = 3600

class Saver:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.abs_file_path = self.create_path()

        self.lines_in_file = 0

    def create_path(self):
        script_dir = os.path.dirname(__file__)  # absolute dir the script is in
        now = str(int(time.time()))
        rel_path = os.path.join("data", "air_data_" + now + ".txt")
        abs_file_path = os.path.join(script_dir, rel_path)
        self.logger.debug('Save data path: ' + abs_file_path)
        return abs_file_path

    def check_file_size_start_new(self):
        self.lines_in_file += 1
        if self.lines_in_file >= MAX_LINES_IN_FILE:
            self.lines_in_file = 0
            self.abs_file_path = self.create_path()

    def save_line(self, data_line):
        self.check_file_size_start_new()
        with open(self.abs_file_path, "a") as file:
            file.write(data_line + '\n')
