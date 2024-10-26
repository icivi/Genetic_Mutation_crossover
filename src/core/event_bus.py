from datetime import datetime
from typing import List, Dict, Callable
import asyncio

class EventBus:
    def __init__(self):
        self.subscribers = {}
        self.message_log = []
        
    async def emit(self, event: str, data: dict):
        message = {
            'event': event,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        self.message_log.append(message)
        
        if event in self.subscribers:
            for callback in self.subscribers[event]:
                await callback(data)
    
    def subscribe(self, event: str, callback: Callable):
        if event not in self.subscribers:
            self.subscribers[event] = []
        self.subscribers[event].append(callback)
    
    def get_recent_events(self, count: int = 10) -> List[Dict]:
        return self.message_log[-count:]