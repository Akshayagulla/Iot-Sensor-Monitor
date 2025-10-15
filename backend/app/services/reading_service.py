from backend.app.repositories import reading_repository

async def add_reading(db, reading_data):
    """Add a new reading to the database."""
    return await reading_repository.create_reading(db, reading_data)

async def get_recent_readings(db, limit=10):
    """Fetch the most recent sensor readings."""
    return await reading_repository.get_latest_readings(db, limit)
