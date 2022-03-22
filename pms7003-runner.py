import serial

from Averager import DictAverager
from Secrets import PIAIR1  # Credential string for MQTT on Thingsboard - don't put credentials in Git
from publish.publisher import Publisher
from sense import Pms7003Sensor, PmsSensorException

if __name__ == '__main__':

    serial_port = '/dev/serial0'  # Raspberry Pi serial port
    serial_device = None
    try:
        serial_device = serial.Serial(port=serial_port, baudrate=9600, bytesize=serial.EIGHTBITS,
                                      parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=2)
    except serial.SerialException:
        print('Could not connect to the serial port')

    sensor = Pms7003Sensor(serial_device)

    pub = Publisher(PIAIR1)
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
            else:
                dict_averager = DictAverager(latest_labelled, 11, call_on_count)
                started = True
            print(latest)
        except PmsSensorException:
            print('Wrong frame length or non-byte value, connection problem?')
        except Exception as ex:
            print('Exception reading the sensor')
            pub.stop()
            sensor.close()
