from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from enum import Enum
from datetime import datetime, timezone

class SensorType(Enum):
    """Enumeration of supported sensor types."""
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"

class BaseSensor(ABC):
    """Simplified base sensor class with metadata for API access."""

    def __init__(self, sensor_id: int, name: str, location: Optional[str] = None):
        self.sensor_id = sensor_id
        self.name = name
        self.location = location

    @property
    @abstractmethod
    def sensor_type(self) -> str:
        """Return the type of this sensor as string."""
        pass

    def get_metadata(self) -> Dict[str, Any]:
        """Return minimal metadata for this sensor."""
        return {
            "sensor_id": str(self.sensor_id),
            "sensor_name": self.name,
            "location": self.location,
            "sensor_type": str(self.sensor_type),
            "path": self.path,
        }

    @abstractmethod
    def generate_reading(self) -> float:
        """Generate a value for this sensor."""
        pass

    def to_payload(self) -> Dict[str, Any]:
        """Convert current reading + metadata to payload."""
        return {
            **self.get_metadata(),
            "value": self.generate_reading(),
            "measured_at": datetime.now(timezone.utc).isoformat()
        }

    @property
    def path(self) -> str:
        """Return a string representation of sensor path."""
        return f"{self.location}/{self.name}({self.sensor_id})"
