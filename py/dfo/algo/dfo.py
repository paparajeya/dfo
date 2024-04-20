from typing import Dict, List
import random

class DFO:
    def __init__(self, *, fitness_func=None, fitness_matrix=None, num_dim: int =2, dims_range: List = [(0,200), (0,300)], num_flies: int = 100, max_iter: int = 20):
        self.__validate_params(fitness_func, fitness_matrix, num_dim, dims_range, num_flies, max_iter)
        self.fitness_func = fitness_func
        self.fitness_matrix = fitness_matrix
        self.num_dim = num_dim
        self.dims_range = dims_range
        self.num_flies = num_flies
        self.max_iter = max_iter
        self.flies: List[Dict] = self.init_flies()
        
    def __validate_params(self, fitness_func, fitness_matrix, num_dim, dims_range, num_flies, max_iter):
        if not isinstance(num_dim, int):
            raise ValueError("num_dim must be an integer")
        if not isinstance(dims_range, (list, tuple)) or not all(isinstance(i, (list, tuple)) for i in dims_range):
            raise ValueError("dims_range must be a list of lists")
        if not isinstance(num_flies, int):
            raise ValueError("num_flies must be an integer")
        if not isinstance(max_iter, int):
            raise ValueError("max_iter must be an integer")
        if fitness_func is None and (fitness_matrix is None or len(fitness_matrix) == 0):
            raise ValueError("Either fitness_func or fitness_matrix must be provided")
        if len(dims_range) != num_dim:
            raise ValueError("Number of dimensions and dims_range must be equal")
        
    def calculate_fitness(self):
        fitness = []
        try:
            for fly in self.flies:
                fitness.append(self.fitness_func(fly))
        except:
            for fly in self.flies:
                fitness.append(self.fitness_matrix[fly[0]][fly[1]])
        return fitness
        
    def init_flies(self):
        flies = []
        for _ in range(self.num_flies):
            pos = self.init_position()
            fitness = self.fitness_func(pos)
            flies.append({"position": pos, "fitness": fitness})
        return flies
    
    def init_position(self):
        pos = []
        for i in range(self.num_dim):
            pos.append(random.uniform(self.dims_range[i][0], self.dims_range[i][1]))
        return pos

    def run(self):
        self.flies = self.init_flies_position()
        self.fitness = self.calculate_fitness()