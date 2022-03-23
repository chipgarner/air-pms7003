import serial
import time
from sense import pms7003


class SensorsBase:
    def get_latest(self) -> dict:
        pass

    def stop(self):
        #  Override to stop any threads
        pass


class PmsSensor(SensorsBase):
    def __init__(self):
        serial_port = '/dev/serial0'  # Raspberry Pi serial port
        try:
            serial_device = serial.Serial(port=serial_port, baudrate=9600, bytesize=serial.EIGHTBITS,
                                          parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=2)
        except serial.SerialException:
            print('Could not connect to the serial porting, try again.')
            time.sleep(1)
             # If this bombs a second time throw the error, this program is useless without any sensors
            serial_device = serial.Serial(port=serial_port, baudrate=9600, bytesize=serial.EIGHTBITS,
                                          parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=2)

        self.sensor = pms7003.Pms7003Sensor(serial_device)

    def get_latest(self):
        return self.sensor.read()

    def stop(self):
        self.sensor.close()  # Close the serial port
