import numpy as np
from typing import List, Tuple, Optional

class NeuralNetwork:
    def __init__(self, layer_sizes: List[int]):
        self.weights = []
        self.biases = []
        
        for i in range(len(layer_sizes) - 1):
            self.weights.append(np.random.randn(layer_sizes[i], layer_sizes[i + 1]) * 0.1)
            self.biases.append(np.random.randn(layer_sizes[i + 1]) * 0.1)
    
    def activate(self, x: np.ndarray) -> np.ndarray:
        return 1 / (1 + np.exp(-x))
    
    def forward(self, inputs: np.ndarray) -> np.ndarray:
        current = inputs
        
        for w, b in zip(self.weights, self.biases):
            current = self.activate(np.dot(current, w) + b)
        
        return current
    
    def mutate(self, mutation_rate: float = 0.1, mutation_range: float = 0.1):
        for i in range(len(self.weights)):
            mask = np.random.random(self.weights[i].shape) < mutation_rate
            self.weights[i] += mask * np.random.randn(*self.weights[i].shape) * mutation_range
            
            mask = np.random.random(self.biases[i].shape) < mutation_rate
            self.biases[i] += mask * np.random.randn(*self.biases[i].shape) * mutation_range
    
    def crossover(self, other: 'NeuralNetwork') -> 'NeuralNetwork':
        if len(self.weights) != len(other.weights):
            raise ValueError("Networks must have same architecture")
        
        child = NeuralNetwork([w.shape[0] for w in self.weights] + [self.weights[-1].shape[1]])
        
        for i in range(len(self.weights)):
            mask = np.random.random(self.weights[i].shape) < 0.5
            child.weights[i] = mask * self.weights[i] + (1 - mask) * other.weights[i]
            
            mask = np.random.random(self.biases[i].shape) < 0.5
            child.biases[i] = mask * self.biases[i] + (1 - mask) * other.biases[i]
        
        return child