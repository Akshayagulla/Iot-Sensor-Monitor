from pydantic import BaseModel

class SensorBase(BaseModel):
    sensor_id: str
    location: str

class SensorCreate(SensorBase):
    pass

class SensorResponse(SensorBase):
    model_config = {"from_attributes": True}
