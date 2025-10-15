from sqlalchemy import select, func
from backend.app.models.reading import Reading
from sqlalchemy.ext.asyncio import AsyncSession

async def get_daily_stats(db: AsyncSession, sensor_id: str):
    """Compute min, max, and avg temperature/humidity for the past 24h."""
    # Placeholder for filtering by last 24 hours
    query = select(
        func.min(Reading.temperature),
        func.max(Reading.temperature),
        func.avg(Reading.temperature),
        func.min(Reading.humidity),
        func.max(Reading.humidity),
        func.avg(Reading.humidity)
    ).where(Reading.sensor_id == sensor_id)

    result = await db.execute(query)
    min_temp, max_temp, avg_temp, min_hum, max_hum, avg_hum = result.one()
    return {
        "min_temp": min_temp,
        "max_temp": max_temp,
        "avg_temp": avg_temp,
        "min_humidity": min_hum,
        "max_humidity": max_hum,
        "avg_humidity": avg_hum,
    }
