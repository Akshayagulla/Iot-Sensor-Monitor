# from typing import Dict, List
# from fastapi import WebSocket
# import asyncio

# class WebSocketManager:
#     def __init__(self):
#         # maps location/type -> list of websocket connections
#         self.active_connections: Dict[str, List[WebSocket]] = {}

#     async def connect(self, websocket: WebSocket, sensor_key: str):
#         await websocket.accept()
#         if sensor_key not in self.active_connections:
#             self.active_connections[sensor_key] = []
#         self.active_connections[sensor_key].append(websocket)

#     def disconnect(self, websocket: WebSocket, sensor_key: str):
#         if sensor_key in self.active_connections:
#             self.active_connections[sensor_key].remove(websocket)
#             if not self.active_connections[sensor_key]:
#                 del self.active_connections[sensor_key]

#     async def broadcast(self, sensor_key: str, message: dict):
#         if sensor_key in self.active_connections:
#             for connection in self.active_connections[sensor_key]:
#                 await connection.send_json(message)


import json

class WebSocketManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def broadcast_json(self, data):
        message = json.dumps(data, default=str)
        await self.broadcast(message)