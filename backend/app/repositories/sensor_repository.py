from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.models.sensor import Sensor

async def get_sensor(db: AsyncSession, sensor_id: str):
    result = await db.execute(select(Sensor).filter(Sensor.sensor_id == sensor_id))
    return result.scalar_one_or_none()

async def create_sensor(db: AsyncSession, sensor_data: dict):
    sensor = Sensor(**sensor_data)
    db.add(sensor)
    await db.commit()
    await db.refresh(sensor)
    return sensor
