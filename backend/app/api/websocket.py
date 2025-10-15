from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.app.utils.websocket_manager import WebSocketManager

router = APIRouter()
manager = WebSocketManager()

@router.websocket("/live")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # optional for bi-directional
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
