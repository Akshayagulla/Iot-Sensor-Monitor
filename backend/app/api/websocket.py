import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.app.utils.websocket_manager import WebSocketManager
from backend.app.services import reading_service
from backend.app.utils.database import get_db

router = APIRouter()
manager = WebSocketManager()

# Global buffer for new readings
batch_buffer = []
BATCH_INTERVAL = 15
STATS_INTERVAL = 300 # 5 minutes

def add_to_batch_buffer(reading):
    batch_buffer.append(reading)

async def broadcast_batched_readings(ts):
    while True:
        await asyncio.sleep(ts)
        if batch_buffer:
            await manager.broadcast_json({"batch": batch_buffer.copy()})
            batch_buffer.clear()

async def broadcast_stats(ts):
    while True:
        await asyncio.sleep(ts)
        # For each sensor, publish updated stats
        async with get_db() as db:
            # You may want to fetch all sensor IDs dynamically
            # For demo, assume you have a list of sensor_ids
            sensor_ids = await reading_service.get_all_sensor_ids(db)
            stats_payload = {}
            for sensor_id in sensor_ids:
                stats = await reading_service.get_stats_for_sensor(db, sensor_id)
                stats_payload[sensor_id] = stats
            await manager.broadcast_json({"stats": stats_payload})

async def start_broadcast_tasks():
    asyncio.create_task(broadcast_batched_readings(BATCH_INTERVAL))
    asyncio.create_task(broadcast_stats(STATS_INTERVAL))

@router.websocket("/live")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)