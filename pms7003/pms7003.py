import pms7003.AqiConverter


class PmsSensorException(Exception):
    """
    Implies a problem with sensor communication that is unlikely to re-occur (e.g. serial connection glitch).
    Prevents from returning corrupt measurements.
    """
    pass


START_SEQ = bytes([0x42, 0x4d])
FRAME_BYTES = 30

BYTES_MEANING = {
    1: 'CF1 1.0 ug/m3',
    2: 'CF1 2.5 ug/m3',
    3: 'CF1 10 ug/m3',
    4: '1.0 ug/m3',
    5: '2.5 ug/m3',
    6: '10 ug/m3',
    7: '0.3 n/dL',
    8: '0.5 n/dL',
    9: '1.0 n/dL',
    10: '2.5 n/dL',
    11: '5.0 n/dL',
    12: '10 n/dL',
}

VALUES = list(BYTES_MEANING.values())

NO_VALUES = len(BYTES_MEANING) + 1


class Pms7003Sensor:

    def __init__(self, serial_device):

        self._serial = serial_device
        self.converter = pms7003.AqiConverter.AqiConverter()

    def _get_frame(self):
        """
        :return: a frame as a list of integer values of bytes
        """
        with self._serial as s:
            s.read_until(START_SEQ)
            frame = list(s.read(FRAME_BYTES))

            return self._check_good_frame(frame)

    @staticmethod
    def _check_good_frame(frame):
        # for index, stuff in enumerate(frame): #Debug
        #     if (index % 2) != 0:
        #         print(int(index / 2), frame[index - 1], stuff)

        if len(frame) == FRAME_BYTES:
            for value in frame:
                if value < 0 or value > 255:
                    print('Error ' + str(value) + ' is not a byte.')
                    raise PmsSensorException
            return frame
        else:
            raise PmsSensorException

    @staticmethod
    def parse_frame(f):
        """
        iterates every second index and glues the H and L bytes together
        :return: raw parsed integer values
        """
        vls = [f[i] << 8 | f[i + 1] for i in range(0, len(f), 2)]
        return vls

    @staticmethod
    def _valid_frame(frame, vls):
        _checksum = vls[-1]
        return _checksum == sum(frame[:-2]) + sum(START_SEQ)

    def get_labeled_values(self, values):

        labeled = {BYTES_MEANING[i]: values[i] for i in range(4, NO_VALUES)} # Ignores CF1 values.

        pm25ug = labeled[BYTES_MEANING[5]]
        pm10ug = labeled[BYTES_MEANING[6]]
        pm25 = self.converter.concentratrion_to_aqi(BYTES_MEANING[5], pm25ug)
        pm10 = self.converter.concentratrion_to_aqi(BYTES_MEANING[6], pm10ug)

        labeled.update({'PM 2.5 EPA': pm25, 'PM 10 EPA': pm10})
        return labeled

    def read(self):
        """
        :return: a dict with measurements or raises Pms7003Exception in case of a problem with connection
        """
        frame = self._get_frame()
        values = self.parse_frame(frame)

        if self._valid_frame(frame, values):
            unlabelled = values[1: NO_VALUES]
            return unlabelled, self.get_labeled_values(values)
        else:
            raise PmsSensorException

    def close(self):
        self._serial.close()
