from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from backend.app.utils.database import Base

class Anomaly(Base):
    __tablename__ = "anomalies"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(String, nullable=False)
    type = Column(String, nullable=False)  # e.g., "temperature_spike"
    value = Column(Float)
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    description = Column(String, nullable=True)
