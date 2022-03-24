from display.MiniDisplay import MiniDisplay
import logging


class Display:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        try:
            self.mini_display = MiniDisplay()
        except:  # If your project is useless without the display don't catch these errors
            self.mini_display = None
            self.logger.exception('Could not initialize display, just keep going without one.')

        self.logger.info('Mini display initialized.')

    def display(self, data: dict):
        if self.mini_display is not None:
            text = 'PM25: ' + str(round(data['PM 2.5 EPA']))
            self.mini_display.display_text(text)
