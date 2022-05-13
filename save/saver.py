import logging
import os


class Saver:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        script_dir = os.path.dirname(__file__)  # absolute dir the script is in
        rel_path = os.path.join("data", "air_data.txt")
        self.abs_file_path = os.path.join(script_dir, rel_path)
        self.logger.debug('Save data path: ' + self.abs_file_path)

    def save_line(self, data_line):
        print(self.abs_file_path)
        with open(self.abs_file_path, "a") as file:
            file.write(data_line + '\n')
