from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "IoT Sensor Monitor"
    DATABASE_URL: str = "sqlite+aiosqlite:///./iot_sensors.db"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
