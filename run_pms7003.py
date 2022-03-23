from sense.sensors import PmsSensor
try:
    from display.display import Display
    display = True
except ModuleNotFoundError:
    display = False  # Assuming this means no display is installed
from publish.publish import Publish


class RunMePms7003:
    def __init__(self):
        self.sensors = PmsSensor()

        if display:
            self.display = Display()
        else:
            self.display = None

        self.publish = Publish()

        self.running = True

    def loop(self):
        while self.running:
            latest = self.sensors.get_latest()
            if self.display is not None:
                self.display.display(latest)
            self.publish.publish(latest)

        self.sensors.stop()


if __name__ == '__main__':
    runner = RunMePms7003()
    runner.loop()