import serial

from pms7003 import Pms7003Sensor, PmsSensorException
from TimeAverager import DictAverager
from publisher import Publisher
from Secrets import PIAIR2
import MiniDisplay

serial_port = '/dev/serial0'
serial_device = serial.Serial(port=serial_port, baudrate=9600, bytesize=serial.EIGHTBITS,
                              parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=2)

if __name__ == '__main__':

    sensor = Pms7003Sensor(serial_device)
    pub = Publisher(PIAIR2)
    display = MiniDisplay.MiniDisplay()
    dict_averager = None

    started = False


    def call_on_count(labelled, delta_t):
        print('Delta t: ' + str(delta_t))
        message = str(labelled)
        pub.send_message(message)
        print(message)


    while True:
        try:
            latest, latest_labelled = sensor.read()
            if started:
                dict_averager.update(latest_labelled)

                text = 'PM25: ' + str(round(latest_labelled['PM 2.5 EPA']))
                display.display_text(text)
            else:
                dict_averager = DictAverager(latest_labelled, 11, call_on_count)
                started = True
            print(latest)
        except PmsSensorException:
            print('Wrong frame length or non-byte value, connection problem?')

    # sensor.close()
    # pub.stop()
