from typing import Dict, List, Optional
import random
import numpy as np
from collections import deque

class BehaviorEngine:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.behaviors = {}
        self.memory = deque(maxlen=1000)
        self.learning_rate = 0.1
        
    def add_behavior(self, name: str, conditions: Dict, actions: List[str], priority: float = 1.0):
        self.behaviors[name] = {
            'conditions': conditions,
            'actions': actions,
            'priority': priority,
            'success_rate': 0.5,
            'usage_count': 0
        }
    
    def evaluate_condition(self, condition: Dict, state: Dict) -> bool:
        operator = condition.get('operator', 'equals')
        value = condition.get('value')
        target = state.get(condition.get('parameter'))
        
        if operator == 'equals':
            return target == value
        elif operator == 'greater':
            return target > value
        elif operator == 'less':
            return target < value
        return False
    
    async def process_state(self, state: Dict) -> List[str]:
        applicable_behaviors = []
        
        for name, behavior in self.behaviors.items():
            conditions_met = all(
                self.evaluate_condition(cond, state)
                for cond in behavior['conditions']
            )
            
            if conditions_met:
                score = behavior['priority'] * behavior['success_rate']
                applicable_behaviors.append((name, score))
        
        if not applicable_behaviors:
            return []
        
        # Select behavior based on scores
        applicable_behaviors.sort(key=lambda x: x[1], reverse=True)
        selected_behavior = self.behaviors[applicable_behaviors[0][0]]
        
        # Update usage statistics
        selected_behavior['usage_count'] += 1
        
        # Store in memory for learning
        self.memory.append({
            'state': state,
            'behavior': selected_behavior,
            'timestamp': state.get('timestamp', 0)
        })
        
        await self.event_bus.emit('behavior-selected', {
            'behavior': selected_behavior,
            'state': state
        })
        
        return selected_behavior['actions']
    
    async def learn_from_memory(self):
        if len(self.memory) < 10:
            return
            
        # Analyze recent memories
        recent_memories = list(self.memory)[-10:]
        
        for memory in recent_memories:
            behavior = memory['behavior']
            state_after = next(
                (m['state'] for m in recent_memories 
                 if m['timestamp'] > memory['timestamp']),
                None
            )
            
            if state_after:
                # Simple success metric
                success = state_after.get('fitness', 0) > memory['state'].get('fitness', 0)
                
                # Update success rate
                old_rate = behavior['success_rate']
                behavior['success_rate'] = (old_rate * (1 - self.learning_rate) + 
                                         success * self.learning_rate)
        
        await self.event_bus.emit('behavior-learning', {
            'behaviors': self.behaviors
        })