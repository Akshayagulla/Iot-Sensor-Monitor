from fastapi import APIRouter, Depends
from backend.app.schemas.reading import ReadingCreate, ReadingResponse
from backend.app.services import reading_service, stats_service
from backend.app.api.websocket import add_to_batch_buffer
from backend.app.utils.database import get_db
import datetime

router = APIRouter()

# @router.post("/ingest", response_model=ReadingResponse)
# async def add_reading(reading: ReadingCreate, db=Depends(get_db)):
#     """Receive new sensor reading."""
#     return await reading_service.add_reading(db, reading.dict())

@router.post("/ingest")
async def add_reading(reading_data: dict, db=Depends(get_db)):
    """Ingest sensor reading from simulator (simplified endpoint)."""
    # Convert simulator format to our reading format
    reading = ReadingCreate(
        sensor_id=reading_data.get("sensor_id"),
        sensor_name=reading_data.get("sensor_name"),
        location=reading_data.get("location"),
        sensor_type=reading_data.get("sensor_type"),
        path=reading_data.get("path"),
        value=reading_data.get("value"),
        measured_at=reading_data.get("measured_at"),
        received_at=datetime.datetime.now(datetime.timezone.utc)
    )

    add_to_batch_buffer(reading.dict())
    return await reading_service.add_reading(db, reading.dict())

@router.get("/latest", response_model=list[ReadingResponse])
async def latest_readings(limit: int = 10, db=Depends(get_db)):
    """Get the most recent readings."""
    return await reading_service.get_recent_readings(db, limit)

@router.get("/stats/{sensor_id}")
async def get_sensor_stats(sensor_id: str, db=Depends(get_db)):
    """Fetch 24-hour stats for a given sensor."""
    return await stats_service.get_daily_stats(db, sensor_id)

# @router.get("/", response_model=List[ReadingResponse])
# async def get_readings(room: str, sensor_type: str, db=Depends(get_db)):
#     return await reading_service.get_readings_by_room_and_type(db, room, sensor_type)
    
@router.get("/historical")
async def get_historical_readings(location: str, type: str, db=Depends(get_db)):
    return await reading_service.get_historical_readings(location, type, db)