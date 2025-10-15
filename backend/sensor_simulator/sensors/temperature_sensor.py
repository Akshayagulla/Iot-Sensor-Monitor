# from base_sensor import BaseSensor, SensorType
# from typing import Optional
# from typing import Dict, Any
# import random

# class TemperatureSensor(BaseSensor):
#     """Temperature sensor implementation.
    
#     Simulates temperature readings in Celsius with realistic ranges
#     for indoor/outdoor environments.
#     """
    
#     def __init__(self, sensor_id: int, name: str, location: Optional[str] = None, 
#                  min_temp: float = -10.0, max_temp: float = 50.0):
#         super().__init__(sensor_id, name, location)
#         self._min_temp = min_temp
#         self._max_temp = max_temp
    
#     @property
#     def sensor_type(self) -> SensorType:
#         return SensorType.TEMPERATURE
    
#     @property
#     def unit(self) -> str:
#         return "°C"
    
#     @property
#     def min_value(self) -> float:
#         return self._min_temp
    
#     @property
#     def max_value(self) -> float:
#         return self._max_temp
    
#     def generate_reading(self) -> float:
#         return round(random.uniform(self.min_value, self.max_value), 2)
    
#     def get_metadata(self) -> Dict[str, Any]:
#         """Return temperature-specific metadata."""
#         metadata = super().get_metadata()
#         metadata.update({
#             "min_temp": self._min_temp,
#             "max_temp": self._max_temp,
#             "description": f"Temperature sensor measuring {self._min_temp}°C to {self._max_temp}°C"
#         })
#         return metadata


import random
from backend.sensor_simulator.base_sensor import BaseSensor, SensorType

class TemperatureSensor(BaseSensor):
    @property
    def sensor_type(self) -> str:
        return str(SensorType.TEMPERATURE.value)

    def generate_reading(self) -> float:
        # Generate a random temperature between 15 and 30 Celsius
        return round(random.uniform(15.0, 30.0), 2)

    @classmethod
    def get_type(cls) -> str:
        return str(SensorType.TEMPERATURE.value)
