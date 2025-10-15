from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.app.config import settings

Base = declarative_base()

engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    from backend.app.models.reading import Reading
    from backend.app.models.sensor import Sensor
    from backend.app.models.anomaly import Anomaly

    """Initialize database and create tables if they don't exist."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created successfully")
    print(engine.url)

# Dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
