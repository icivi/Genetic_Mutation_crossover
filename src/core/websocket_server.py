import asyncio
import json
import websockets
from typing import Set, Dict

class WebSocketServer:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.server = None
    
    async def register(self, websocket):
        self.clients.add(websocket)
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self.event_bus.emit('external-input', data)
                except json.JSONDecodeError:
                    pass
        finally:
            self.clients.remove(websocket)
    
    async def broadcast(self, message: Dict):
        if not self.clients:
            return
        
        websockets_tasks = []
        for client in self.clients:
            websockets_tasks.append(
                asyncio.create_task(
                    client.send(json.dumps(message))
                )
            )
        await asyncio.gather(*websockets_tasks)
    
    async def start(self, host: str, port: int):
        self.event_bus.subscribe('system-update', self.broadcast)
        self.server = await websockets.serve(self.register, host, port)
        print(f"WebSocket server started on ws://{host}:{port}")
    
    async def stop(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()