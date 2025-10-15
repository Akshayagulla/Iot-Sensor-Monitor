from fastapi import APIRouter, Depends, Query, HTTPException
from backend.app.utils.database import get_db
from backend.app.repositories import reading_repository
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from collections import defaultdict
import statistics
from sqlalchemy import select, func
from backend.app.models.reading import Reading

async def add_reading(db, reading_data):
    """Add a new reading to the database."""
    return await reading_repository.create_reading(db, reading_data)

async def get_recent_readings(db, limit=10):
    """Fetch the most recent sensor readings."""
    return await reading_repository.get_latest_readings(db, limit)

# async def get_readings_by_room_and_type(
#     room: str = Query(..., alias="room"),
#     sensor_type: str = Query(..., alias="type"),
#     db=Depends(get_db)
# ):
#     return await reading_repository.get_readings_by_room_and_type(db, room, sensor_type)

def compute_statistics(readings, now):
    # 2. Prepare readings for response
    readings_list = [
        {"timestamp": r.measured_at.isoformat() + "Z", "value": r.value}
        for r in readings
    ]

    # 3. Compute stats for each interval
    def compute_stats(interval_minutes):
        cutoff = now - timedelta(minutes=interval_minutes)
        values = [
            r.value
            for r in readings
            if (
                (r.measured_at.replace(tzinfo=timezone.utc) if r.measured_at.tzinfo is None else r.measured_at)
                >= cutoff
            )
        ]
        if not values:
            return {"min": None, "max": None, "avg": None}
        return {
            "min": min(values),
            "max": max(values),
            "avg": round(statistics.mean(values), 2)
        }

    stats = {
        "5min": compute_stats(5),
        "1hr": compute_stats(60),
        "6hr": compute_stats(360),
        "1day": compute_stats(1440),
    }

    # 4. Compose response
    return {
        "readings": readings_list,
        "stats": stats
    }

async def get_all_sensor_ids(db):
    """Return a list of all unique sensor IDs."""
    result = await db.execute(select(Reading.sensor_id).distinct())
    sensor_ids = [row[0] for row in result.fetchall()]
    return sensor_ids

async def get_stats_for_sensor(db, sensor_id):
    """Return min, max, avg for the last 24h for a given sensor."""
    now = datetime.now(timezone.utc)
    since = now - timedelta(days=1)

    readings = await reading_repository.get_readings_by_sensor_id(db, sensor_id, since)
    # readings is already a list
    return compute_statistics(readings, now)["stats"]

async def get_historical_readings(
    location: str = Query(...),
    type: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    # 1. Query readings from the last 24 hours
    now = datetime.now(timezone.utc)
    since = now - timedelta(days=1)
    readings = await reading_repository.get_readings_by_location_and_type(
        db, location, type, since
    )
    readings = readings.scalars().all()
    if not readings:
        raise HTTPException(status_code=404, detail="No readings found")
    readings = readings[-20:] # Limit to last 20 readings

    result = compute_statistics(readings, now)
    return {
        "sensor_id": readings[0].sensor_id if readings else None,
        "readings": result["readings"][-20:],
        "stats": result["stats"]
    }