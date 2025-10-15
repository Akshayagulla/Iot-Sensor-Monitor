import asyncio
from backend.app.utils.database import Base, engine

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created successfully")
    print(engine.url)

if __name__ == "__main__":
    asyncio.run(init_db())
