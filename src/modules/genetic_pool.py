import random
from typing import Dict, List, Optional
import numpy as np

class GeneticPool:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.population = []
        self.generation = 0
        self.mutation_rate = 0.1
        
    def create_individual(self, genes: Dict) -> Dict:
        return {
            'genes': genes,
            'fitness': 0,
            'generation': self.generation,
            'ancestors': []
        }
    
    def mutate(self, genes: Dict) -> Dict:
        mutated = genes.copy()
        for key in mutated:
            if isinstance(mutated[key], (int, float)):
                if random.random() < self.mutation_rate:
                    mutated[key] *= random.uniform(0.8, 1.2)
            elif isinstance(mutated[key], bool):
                if random.random() < self.mutation_rate:
                    mutated[key] = not mutated[key]
        return mutated
    
    def crossover(self, parent1: Dict, parent2: Dict) -> Dict:
        child_genes = {}
        all_keys = set(parent1['genes'].keys()) | set(parent2['genes'].keys())
        
        for key in all_keys:
            if random.random() < 0.5:
                child_genes[key] = parent1['genes'].get(key)
            else:
                child_genes[key] = parent2['genes'].get(key)
        
        return self.create_individual(child_genes)
    
    async def evolve(self):
        if len(self.population) < 2:
            return
        
        # Sort by fitness
        self.population.sort(key=lambda x: x['fitness'], reverse=True)
        
        # Select top performers
        elite_size = max(2, len(self.population) // 10)
        elite = self.population[:elite_size]
        
        # Create new generation
        new_population = elite.copy()
        
        while len(new_population) < len(self.population):
            parent1 = random.choice(elite)
            parent2 = random.choice(elite)
            child = self.crossover(parent1, parent2)
            child['genes'] = self.mutate(child['genes'])
            new_population.append(child)
        
        self.population = new_population
        self.generation += 1
        
        await self.event_bus.emit('evolution-step', {
            'generation': self.generation,
            'population_size': len(self.population),
            'best_fitness': elite[0]['fitness']
        })