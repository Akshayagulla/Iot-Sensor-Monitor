from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.sql import func
from backend.app.utils.database import Base

class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(String, ForeignKey("sensors.sensor_id"), nullable=False)
    sensor_name = Column(String)   # <- add this column
    location = Column(String)      # optional, if you want
    sensor_type = Column(String)   # optional
    path = Column(String)          # optional
    value = Column(Float)
    measured_at = Column(DateTime)
    received_at = Column(DateTime)
