from pydantic import BaseModel
from datetime import datetime

class ReadingBase(BaseModel):
    sensor_id: str
    sensor_name: str
    location: str
    sensor_type: str
    path: str
    value: float
    measured_at: datetime
    received_at: datetime

class ReadingCreate(ReadingBase):
    pass

class ReadingResponse(ReadingBase):
    id: int
    timestamp: datetime

    model_config = {"from_attributes": True}
