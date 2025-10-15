from fastapi import APIRouter, Depends, HTTPException
from backend.app.schemas.sensor import SensorCreate, SensorResponse
from backend.app.repositories import sensor_repository
from backend.app.utils.database import get_db

router = APIRouter()

@router.post("/", response_model=SensorResponse)
async def register_sensor(sensor: SensorCreate, db=Depends(get_db)):
    existing = await sensor_repository.get_sensor(db, sensor.sensor_id)
    if existing:
        raise HTTPException(status_code=400, detail="Sensor already exists")
    return await sensor_repository.create_sensor(db, sensor.dict())
