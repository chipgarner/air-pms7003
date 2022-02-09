from TimeAverager import DictAverager


class Average:
    def __init__(self):
        self.answer = {}
        self.delta_time = 0

    def average(self, avg, delta_t):
        print("Average: " + str(avg) + " Timespan: " + str(delta_t))
        self.answer = avg
        self.delta_time = delta_t


def test_it_averages():
    avg = Average()
    info = {'Big': 1, 'fat': 22, 'fake': 7}
    dict_average = DictAverager(info, 2, avg.average)

    dict_average.update(info)

    assert avg.answer == {}

    info = {'Big': 2, 'fat': 11, 'fake': 9}
    dict_average.update(info)

    assert avg.answer == {'Big': 1.5, 'fat': 16.5, 'fake': 8.0}
    assert avg.delta_time == 0


def test_it_averages_more():
    avg = Average()
    info = {'Big': 1, 'fat': 1, 'fake': 1}
    dict_average = DictAverager(info, 5, avg.average)

    for i in range(5):
        info = {'Big': 1+i, 'fat': 1+i, 'fake': 1+i}
        dict_average.update(info)

    assert avg.answer == {'Big': 3.0, 'fake': 3.0, 'fat': 3.0}


def test_missing_data_works():
    avg = Average()
    info = {'Big': 1, 'fat': 1, 'fake': 1}
    dict_average = DictAverager(info, 5, avg.average)

    for i in range(4):
        info = {'Big': 1, 'fat': 1, 'fake': 1}
        dict_average.update(info)

    info = {'Big': 1, 'fake': 1}
    dict_average.update(info)

    assert avg.answer == {'Big': 1.0, 'fake': 1.0, 'fat': 1.0}
    assert avg.delta_time == 0


def test_extra_dict_key_ignored():
    avg = Average()
    info = {'Big': 1, 'fake': 7}
    dict_average = DictAverager(info, 2, avg.average)

    dict_average.update(info)

    assert avg.answer == {}

    info = {'Big': 2, 'fat': 11, 'fake': 9}
    dict_average.update(info)

    assert avg.answer == {'Big': 1.5, 'fake': 8.0}
    assert avg.delta_time == 0


def test_starts_over():
    avg = Average()
    info = {'Big': 1, 'fat': 1, 'fake': 1}
    dict_average = DictAverager(info, 4, avg.average)

    for i in range(4):
        info = {'Big': 1, 'fat': 1, 'fake': 1}
        dict_average.update(info)

    assert dict_average.averagers['Big'].count == 0

    assert avg.answer == {'Big': 1.0, 'fake': 1.0, 'fat': 1.0}
    assert avg.delta_time == 0

    info = {'Big': 2, 'fat': 2, 'fake': 2}
    dict_average.update(info)

    assert dict_average.averagers['Big'].count == 1
