from display.MiniDisplay import MiniDisplay


class Display:
    def __init__(self):
        try:
            self.mini_display = MiniDisplay()
        except:
            self.mini_display = None
            print('Could not initialize display, just keep going')

    def display(self, data: dict):
        if self.mini_display is not None:
            text = 'PM25: ' + str(round(data['PM 2.5 EPA']))
            self.mini_display.display_text(text)
