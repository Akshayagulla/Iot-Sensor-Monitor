# from __future__ import annotations

# """SQLAlchemy models for sensors.

# Defines the `Sensor` entity and shared declarative `Base`. Field types and
# nullability capture basic validation at the database level (e.g., `name` is
# required, `location` optional). Higher-level input validation is handled in
# Pydantic schemas used by the API layer.
# """

# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
# from sqlalchemy import String, DateTime, func, Enum, Column
# from typing import List, Optional
# import enum

# from backend.app.utils.database import Base


# class Base(DeclarativeBase):
#     """Base class for all ORM models."""
#     pass


# class SensorType(enum.Enum):
#     """Enumeration of supported sensor types."""
#     TEMPERATURE = "temperature"
#     HUMIDITY = "humidity"

# class Sensor(Base):
#     __tablename__ = "sensors"

#     sensor_id = Column(String, primary_key=True, index=True)
#     location = Column(String, nullable=False)

# backend/app/models/sensor.py
from sqlalchemy import Column, String
from backend.app.utils.database import Base  # ✅ Use the same Base as Reading

class Sensor(Base):
    __tablename__ = "sensors"

    sensor_id = Column(String, primary_key=True, index=True)
    location = Column(String, nullable=False)
