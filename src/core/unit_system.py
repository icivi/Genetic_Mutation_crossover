import uuid
from datetime import datetime
from typing import Dict, Optional

class UnitSystem:
    def __init__(self, event_bus):
        self.units = {}
        self.event_bus = event_bus
        self.setup_event_listeners()
    
    def setup_event_listeners(self):
        self.event_bus.subscribe('external-input', self.handle_external_input)
        self.event_bus.subscribe('unit-mutation', self.handle_unit_mutation)
    
    async def create_unit(self, unit_type: str, properties: Dict = None):
        unit = {
            'id': str(uuid.uuid4()),
            'type': unit_type,
            'properties': properties or {},
            'created': datetime.now().isoformat(),
            'fitness': 0,
            'generation': 1
        }
        
        self.units[unit['id']] = unit
        await self.event_bus.emit('unit-created', unit)
        return unit
    
    async def handle_external_input(self, data: Dict):
        if data.get('type') == 'create-unit':
            await self.create_unit(data.get('unit_type'), data.get('properties'))
    
    async def handle_unit_mutation(self, data: Dict):
        unit_id = data.get('unit_id')
        if not unit_id or unit_id not in self.units:
            return
            
        unit = self.units[unit_id]
        mutated_properties = self.mutate_properties(unit['properties'])
        unit['properties'] = mutated_properties
        unit['generation'] += 1
        
        await self.event_bus.emit('system-update', {
            'type': 'unit-mutated',
            'unit': unit
        })
    
    def mutate_properties(self, properties: Dict) -> Dict:
        return {
            **properties,
            'mutation_count': properties.get('mutation_count', 0) + 1,
            'last_mutation': datetime.now().isoformat()
        }