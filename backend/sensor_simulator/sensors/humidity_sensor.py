import random
from backend.sensor_simulator.base_sensor import BaseSensor, SensorType

class HumiditySensor(BaseSensor):
    @property
    def sensor_type(self) -> str:
        return str(SensorType.HUMIDITY.value)

    def generate_reading(self) -> float:
        # Generate a random humidity percentage between 30% and 70%
        return round(random.uniform(30.0, 70.0), 2)

    @classmethod
    def get_type(cls) -> str:
        return str(SensorType.HUMIDITY.value)
