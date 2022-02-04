import time


class TimeAverager:
    def __init__(self, num, call_on_average):
        self.on_average = call_on_average
        self.num = num

        self.sum = None
        self.count = None
        self.start_time = None
        self.init()

    def init(self):
        self.sum = 0
        self.count = 0
        self.start_time = time.time()

    def update_average(self, value):
        self.count += 1
        self.sum = self.sum + value
        if self.count >= self.num:
            avg = self.sum / self.num
            delta_t = time.time() - self.start_time

            self.on_average(avg, delta_t)

class DictAverager:
    def __init__(self):
        pass