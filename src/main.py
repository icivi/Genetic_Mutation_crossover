import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, Optional

from core.event_bus import EventBus
from core.unit_system import UnitSystem
from core.websocket_server import WebSocketServer

async def main():
    # Initialize core systems
    event_bus = EventBus()
    unit_system = UnitSystem(event_bus)
    
    # Start WebSocket server
    server = WebSocketServer(event_bus)
    await server.start('localhost', 8765)
    
    try:
        # Keep the server running
        await asyncio.Future()  # run forever
    except KeyboardInterrupt:
        await server.stop()

if __name__ == "__main__":
    asyncio.run(main())