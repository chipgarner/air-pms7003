class RunMeInterface:
    def init_sensors(self) -> bool:  # True is success
        pass

    def get_latest_sensor_data(self) -> dict:
        pass

    def init_display(self) -> bool:
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
