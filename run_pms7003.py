import runmeinterface
import serial
from sense import Pms7003Sensor, PmsSensorException


class RunMePms7003(runmeinterface.RunMeInterface):
    def __init__(self):
        self.sensor = None

    def init_sensors(self) -> bool:

        serial_port = '/dev/serial0'  # Raspberry Pi serial port
        serial_device = None
        try:
            serial_device = serial.Serial(port=serial_port, baudrate=9600, bytesize=serial.EIGHTBITS,
                                          parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=2)
        except serial.SerialException:
            print('Could not connect to the serial port')
            return False

        self.sensor = Pms7003Sensor(serial_device)

        return True

    def get_latest_sensor_data(self) -> dict:
        return self.sensor.read()
