import Averager as Avg


class Average:
    def __init__(self):
        self.answer = 0
        self.delta_time = 0

    def average(self, avg, delta_t):
        print("Average: " + str(avg) + " Timespan: " + str(delta_t))
        self.answer = avg
        self.delta_time = delta_t


def test_averager():
    avg = Average()
    averager = Avg.TimeAverager(1, avg.average)

    averager.update_average(12.345)

    assert avg.answer == 12.345
    assert avg.delta_time > 0


def test_averager_averages():
    avg = Average()
    averager = Avg.TimeAverager(10, avg.average)

    averager.update_average(1)

    assert avg.answer == 0
    assert avg.delta_time == 0

    for i in range(2, 10):
        averager.update_average(i)
        assert avg.answer == 0
        assert avg.delta_time == 0

    averager.update_average(10)

    assert avg.answer == 5.5
    assert avg.delta_time > 0


def test_averager_function_none():
    averager = Avg.TimeAverager(1, None)

    averager.update_average(12.345)
