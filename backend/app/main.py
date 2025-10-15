from fastapi import FastAPI
from backend.app.api import sensors, readings, websocket
from backend.app.utils.database import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ This replaces startup event
    await startup_event()
    yield  # App runs here

async def startup_event():
    await init_db()
    await websocket.start_broadcast_tasks()

# Pass lifespan to FastAPI so it runs at startup
server = FastAPI(
    title="IoT Sensor Monitor API",
    version="1.0",
    lifespan=lifespan
)

# Include API routers
server.include_router(sensors.router, prefix="/api/v1/sensors", tags=["Sensors"])
server.include_router(readings.router, prefix="/api/v1/readings", tags=["Readings"])
server.include_router(websocket.router, prefix="/api/v1/ws", tags=["WebSocket"])

@server.get("/")
async def root():
    return {"message": "IoT Sensor Monitor Backend is running 🚀"}
