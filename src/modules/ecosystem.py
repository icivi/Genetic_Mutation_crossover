from typing import Dict, List, Optional
import random
import numpy as np

class Ecosystem:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.species = {}
        self.relationships = {}
        self.resources = {}
        
    async def add_species(self, name: str, properties: Dict):
        self.species[name] = {
            'properties': properties,
            'population': 100,
            'fitness': 0,
            'adaptation_level': 0
        }
        
        await self.event_bus.emit('species-added', {
            'name': name,
            'properties': properties
        })
    
    def add_relationship(self, species1: str, species2: str, relationship_type: str):
        if species1 not in self.species or species2 not in self.species:
            return
            
        key = f"{species1}:{species2}"
        self.relationships[key] = {
            'type': relationship_type,
            'strength': random.random(),
            'stability': random.random()
        }
    
    async def simulate_step(self):
        # Update populations based on relationships
        for key, rel in self.relationships.items():
            species1, species2 = key.split(':')
            
            if rel['type'] == 'competition':
                # Reduce both populations
                factor = rel['strength'] * 0.1
                self.species[species1]['population'] *= (1 - factor)
                self.species[species2]['population'] *= (1 - factor)
            
            elif rel['type'] == 'cooperation':
                # Increase both populations
                factor = rel['strength'] * 0.1
                self.species[species1]['population'] *= (1 + factor)
                self.species[species2]['population'] *= (1 + factor)
        
        # Natural selection and adaptation
        for name, species in self.species.items():
            if species['population'] > 0:
                # Random environmental pressure
                pressure = random.random()
                adaptation = species['adaptation_level']
                
                if pressure > adaptation:
                    # Species needs to adapt
                    species['adaptation_level'] += 0.1 * (pressure - adaptation)
                    species['fitness'] += 0.05
                else:
                    species['fitness'] -= 0.02
                
                # Population growth/decline
                growth_rate = 0.1 * (species['fitness'] + species['adaptation_level'])
                species['population'] *= (1 + growth_rate)
                
                # Cap population
                species['population'] = min(1000, max(0, species['population']))
        
        await self.event_bus.emit('ecosystem-update', {
            'species': self.species,
            'relationships': self.relationships
        })