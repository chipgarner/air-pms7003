from pms7003 import Pms7003Sensor, PmsSensorException
from pms7003.publisher import Publisher
import serial

serial_port = '/dev/serial0'
serial_device = serial.Serial(port=serial_port, baudrate=9600, bytesize=serial.EIGHTBITS,
                             parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=2)


if __name__ == '__main__':

    sensor = Pms7003Sensor(serial_device)
    pub = Publisher()

    while True:
        try:
            latest, latest_labelled = sensor.read()
            message = str(latest_labelled)
            pub.send_message(message)
            print(latest_labelled)
            print(latest)
        except PmsSensorException:
            print('Wrong frame length or non-byte value, connection problem?')

    sensor.close()
    pub.stop()
