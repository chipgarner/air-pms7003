import sense


class FakeSerial:
    def __enter__(self):  # So "with" works
        pass
        return self

    def __exit__(self, this, that, the_other):
        pass

    def read_until(self, later):
        pass

    def read(self, num_bytes):
        return [1, 2,
                3, 4,
                0, 1,
                1, 0,
                0, 255,
                255, 0,
                255, 255,
                0, 1,
                0, 20,
                21, 22,
                23, 24,
                25, 26,
                27, 28,
                29, 10,
                10, 10]


def test_parser():
    sensor = sense.Pms7003Sensor(None)

    frame = [0x42, 0x4d, 3, 4, 5, 6, 7, 8, -99, 10, 11, 12, 13, 14]
    parsed = sensor.parse_frame(frame)

    print('whoopy')
    print(type(parsed))
    print(len(parsed))
    for stuff in parsed:
        print(stuff)
    print(parsed[0:20])

    assert parsed[4] == -25334  # It works for non-bytes


def test_it_more():
    fake = FakeSerial()
    sensor = sense.Pms7003Sensor(fake)

    frame = sensor._get_frame()

    try:
        parsed = sensor.parse_frame(frame)
    except sense.PmsSensorException:
        print('Threw and caught the error.')

    print('')
    print(parsed[0:14])

    assert parsed[0] == 258
    assert parsed[1] == 772
    assert parsed[2] == 1
    assert parsed[3] == 256
    assert parsed[4] == 255
    assert parsed[5] == 65280
    assert parsed[6] == 65535


def test_throws_not_a_byte():
    fake = FakeSerial()
    sensor = sense.Pms7003Sensor(fake)

    frame = sensor._get_frame()
    frame[17] = -20

    try:
        parsed = sensor._check_good_frame(frame)
    except sense.PmsSensorException:
        print('Throw and caught the error.')

    frame[17] = 20  # Frame is good, continues inn loop
    parsed = sensor.parse_frame(frame)

    print('')
    print(parsed[0:14])

    assert parsed[0] == 258
    assert parsed[1] == 772
    assert parsed[2] == 1
    assert parsed[3] == 256
    assert parsed[4] == 255
    assert parsed[5] == 65280
    assert parsed[6] == 65535


def test_get_labeled_values():
    fake = FakeSerial()
    sensor = sense.Pms7003Sensor(fake)

    frame = sensor._get_frame()

    labelled = sensor.get_labeled_values(frame)

    assert labelled == {'1.0 ug/m3': 0, '2.5 ug/m3': 1, '10 ug/m3': 1, '0.3 n/dL': 0,
                        '0.5 n/dL': 0, '1.0 n/dL': 255, '2.5 n/dL': 255, '5.0 n/dL': 0,
                        '10 n/dL': 255, 'PM 10 EPA': 1, 'PM 2.5 EPA': 4}

