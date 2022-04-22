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
            avg, delta_t = self.get_result()

            if self.on_average is not None:
                self.on_average(avg, delta_t)

    def get_result(self):
        avg = self.sum / self.count
        delta_t = time.time() - self.start_time
        return avg, delta_t


class DictAverager:
    def __init__(self, numbers_dict, num, call_on_average):
        self.on_average = call_on_average

        self.the_keys = numbers_dict.keys()
        self.averagers = {}
        for each_key in self.the_keys:
            self.averagers.update({each_key: TimeAverager(num, None)})

    def update(self, numbers_dict):
        done = False
        for key in numbers_dict:  # Update only the incoming dict in case an item is missing
            if key in self.the_keys:
                self.averagers[key].update_average(numbers_dict[key])
                if self.averagers[key].count >= self.averagers[key].num:
                    done = True

        if done:
            results = {}
            for key in self.the_keys:  # Compute and report for the original dict.
                average, delta_t = self.averagers[key].get_result()
                results.update({key: average})

                self.averagers[key].init()

            time_stamped_results = {"ts": round(time.time() * 1000), "values": results}
            print(time_stamped_results)
            self.on_average(results, round(delta_t))
