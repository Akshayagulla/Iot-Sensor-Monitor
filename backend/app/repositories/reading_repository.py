from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from backend.app.models.reading import Reading

async def create_reading(db: AsyncSession, reading_data: dict):
    reading = Reading(**reading_data)
    db.add(reading)
    await db.commit()
    await db.refresh(reading)
    return reading

async def get_latest_readings(db: AsyncSession, limit: int = 10):
    result = await db.execute(select(Reading).order_by(Reading.timestamp.desc()).limit(limit))
    return result.scalars().all()

async def get_readings_by_sensor_id(db, sensor_id, since):
    '''Fetch all readings filtered by room and sensor type.'''
    stmt = select(Reading).where(Reading.sensor_id == sensor_id).where(Reading.measured_at >= since).order_by(Reading.measured_at)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_readings_by_location_and_type(db, location, type, since):
    '''Fetch readings filtered by location and type since a given time.'''
    print("accessing repository function")
    return await db.execute(
        select(Reading)
        .where(Reading.location == location)
        .where(Reading.sensor_type == type)
        .where(Reading.measured_at >= since)
        .order_by(Reading.measured_at)
    )
    print("fetched data from db")
    return result.scalars().all()