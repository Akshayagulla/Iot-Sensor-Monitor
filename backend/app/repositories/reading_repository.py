from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
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
