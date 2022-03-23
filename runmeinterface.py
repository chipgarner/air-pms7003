class DeviceBase:
    def initialize(self) -> bool:  # True is success
        #  For initializations that don't belong in the def __init__
        pass

    def stop(self):
        #  Write a stop function for devices that run on threads
        pass


class RunMeInterface:
    def init_sensors(self) -> bool:  # True is success
        pass

    def get_latest_sensor_data(self) -> dict:
        #  You probably need to override this or the program won't do much
        pass

    def init_display(self) -> bool:
        #  Ignore display functions if you don't have a display
        pass

    def display(self, sensor_data: dict):
        pass

    def init_publisher(self) -> bool:
        pass

    def publish(self, sensor_data: dict):
        pass

    def init_storage(self) -> bool:
        pass

    def store(self, sensor_data: dict):
        pass

    def main_loop(self):
        pass
