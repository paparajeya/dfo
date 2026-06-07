# -*- coding: utf-8 -*-
"""Driver Program for Dispersive Fly Optimisation (DFO) algorithm.

@Author     : Dr Prashant Aparajeya
                Founder & Director @AISimply Ltd
                Computer Vision Scientist
                London, United Kingdom

@Credits    : Dr. Mohammad Majid al-Rifaie
                Associate Professor in Computer Science
                Greenwich University, London, UK
                
@Copyright  : Copyright 2024 - present
@Project    : Dispersive Flies Optimisation (DFO) Algorithm
"""

import logging
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_NUM_FLIES = 100
DEFAULT_MAX_ITERATIONS = 1000
DEFAULT_DISTRIBUTION_THRESHOLD = 0.0001
DEFAULT_FITNESS_FUNCTION_TYPE = 'min'  # or 'max'

@dataclass
class Fly:
    """Class representing a fly in the DFO algorithm."""
    idx: int
    position: np.ndarray
    fitness: float = None
    left: List[int] = None # List of indices of the best flies to the left in each dimension
    right: List[int] = None # List of indices of the best flies to the right in each dimension


class DFO:
    """Dispersive Fly Optimisation (DFO) Algorithm.

    This class implements the DFO algorithm for optimisation problems.
    """

    def __init__(
        self,
        *, 
        fitness_function: callable = None,
        fitness_matrix: np.ndarray = None,
        fitness_function_type: str = None,
        dims_range: List[Tuple[float | int, float | int]] = None,
        num_flies: int = None, 
        max_iterations: int = None,
        distribution_threshold: float = None,
    ):
        """Initialises the DFO algorithm.

        Args:
            fitness_function (callable): The fitness function to evaluate solutions.
            fitness_matrix (np.ndarray): The fitness matrix to evaluate solutions.
            dims_range (List[Tuple[float | int, float | int]]): The range of dimensions for the search space.
            num_flies (int): The number of flies in the population.
            max_iterations (int): The maximum number of iterations to run the algorithm.
            distribution_threshold (float): The threshold for distribution.
            fitness_function_type (str): The type of fitness function ('min' or 'max').
        """
        self._init_validate_inputs(
            fitness_function=fitness_function,
            fitness_matrix=fitness_matrix,
            dims_range=dims_range,
            num_flies=num_flies,
            max_iterations=max_iterations,
            distribution_threshold=distribution_threshold,
            fitness_function_type=fitness_function_type
        )
        self._init_flies()
        self.get_best_fly()

    def _init_validate_inputs(self, **kwargs):
        """Validate the input parameters for the DFO algorithm."""
        # Either fitness_function or fitness_matrix must be provided, if both then fitness_function takes precedence
        if not kwargs.get('fitness_function') and not kwargs.get('fitness_matrix'):
            raise ValueError("Either 'fitness_function' or 'fitness_matrix' must be provided.")
        if kwargs.get('fitness_function') and not callable(kwargs.get('fitness_function')):
            raise ValueError("'fitness_function' must be a callable function.")
        else:
            self.fitness_function = kwargs.get('fitness_function')

        if kwargs.get('fitness_matrix') is not None and not isinstance(kwargs.get('fitness_matrix'), np.ndarray):
            raise ValueError("'fitness_matrix' must be a numpy array.")
        else:
            self.fitness_matrix = kwargs.get('fitness_matrix')
            
        if kwargs.get('dims_range') is None and self.fitness_matrix is None:
            raise ValueError("'dims_range' must be provided if 'fitness_matrix' is not provided.")
        elif kwargs.get('dims_range') is not None and not isinstance(kwargs.get('dims_range'), (list, tuple)):
            # If the fitness matrix is provided, we can infer the dims_range from its shape
            if self.fitness_matrix is not None:
                self.dims_range = []
                for d in self.fitness_matrix.shape:
                    self.dims_range.append((0, d-1))  # Assuming the search space is from 0 to d-1 for each dimension
            else:
                raise ValueError("'dims_range' must be a list or tuple.")
        else:
            self.dims_range = kwargs.get('dims_range')

        if kwargs.get('num_flies') is None:
            logger.warning(f"'num_flies' not provided. Using default value of `{DEFAULT_NUM_FLIES}`.")
            self.num_flies = DEFAULT_NUM_FLIES
        elif not isinstance(kwargs.get('num_flies'), int) or kwargs.get('num_flies') <= 0:
            raise ValueError("'num_flies' must be a positive integer.")
        else:
            self.num_flies = kwargs.get('num_flies')

        if kwargs.get('max_iterations') is None:
            logger.warning(f"'max_iterations' not provided. Using default value of `{DEFAULT_MAX_ITERATIONS}`.")
            self.max_iterations = DEFAULT_MAX_ITERATIONS
        elif not isinstance(kwargs.get('max_iterations'), int) or kwargs.get('max_iterations') <= 0:
            raise ValueError("'max_iterations' must be a positive integer.")
        else:
            self.max_iterations = kwargs.get('max_iterations')

        if kwargs.get('fitness_function_type') is None:
            logger.warning(f"'fitness_function_type' not provided. Using default value of `{DEFAULT_FITNESS_FUNCTION_TYPE}`.")
            self.fitness_function_type = DEFAULT_FITNESS_FUNCTION_TYPE
        elif kwargs.get('fitness_function_type') not in ['min', 'max']:
            raise ValueError("'fitness_function_type' must be either 'min' or 'max'.")
        else:
            self.fitness_function_type = kwargs.get('fitness_function_type')

        if kwargs.get('distribution_threshold') is None:
            logger.warning(f"'distribution_threshold' not provided. Using default value of `{DEFAULT_DISTRIBUTION_THRESHOLD}`.")
            self.distribution_threshold = DEFAULT_DISTRIBUTION_THRESHOLD
        elif not isinstance(kwargs.get('distribution_threshold'), (int, float)) or kwargs.get('distribution_threshold') <= 0:
            raise ValueError("'distribution_threshold' must be a positive number.")
        else:
            self.distribution_threshold = kwargs.get('distribution_threshold')

    def _init_flies(self):
        """Initialises the flies in the search space."""
        self.flies = []
        for idx in range(self.num_flies):
            fly_position = np.random.uniform(
                low=[low for low, _ in self.dims_range],
                high=[high for _, high in self.dims_range]
            )
            fitness = self.calculate_fitness(fly_position)
            self.flies.append(
                Fly(
                    idx=idx, 
                    position=fly_position, 
                    fitness=fitness, 
                    left=[], 
                    right=[]
                )
            )
        
        # Initialises the best flies to the left and right for each fly in each dimension randomly 
        # but ensuring they are different from the fly itself. 
        
        # Going though each dimension
        for _ in range(len(self.dims_range)):
            idxs = self._shuffle_indices()
            
            for i in range(self.num_flies):
                fly_idx = np.where(idxs == i)[0][0]  # Get the index of the fly in the shuffled order
                self.flies[i].left.append(int((self.num_flies + idxs[fly_idx-1]) % self.num_flies))  # Previous fly in the shuffled order is the left best fly
                self.flies[i].right.append(int(idxs[(fly_idx+1) % self.num_flies]))  # Next fly in the shuffled order is the right best fly

        # Print files
        # logger.info(f"Initialised Flies:{self.flies}")

    def _shuffle_indices(self) -> np.ndarray:
        idxs = np.arange(self.num_flies, dtype=int)
        # Shuffle the indices to randomise the order of flies
        is_valid_shuffle = False

        while not is_valid_shuffle:
            np.random.shuffle(idxs)
            # Check if any fly is assigned itself as left or right best fly
            is_valid_shuffle = True
            
            for i in range(self.num_flies):
                fly_idx = np.where(idxs == i)[0][0]  # Get the index of the fly in the shuffled order
                left_idx = (self.num_flies + idxs[fly_idx-1]) % self.num_flies  # Previous fly in the shuffled order is the left best fly
                right_idx = idxs[(fly_idx+1) % self.num_flies]  # Next fly in the shuffled order is the right best fly
                if left_idx == i or right_idx == i:
                    is_valid_shuffle = False
                    break  # If any fly is assigned itself, reshuffle and check again
        
        return idxs

    def _validate_position(self, position):
        """Validate the position of a fly in the search space."""
        if not isinstance(position, (list, np.ndarray)):
            raise ValueError("Position must be a list or numpy array.")
        if len(position) != len(self.dims_range):
            raise ValueError(f"Position must have the same number of dimensions as 'dims_range' ({len(self.dims_range)}).")
        for i, (low, high) in enumerate(self.dims_range):
            if not (low <= position[i] <= high):
                raise ValueError(f"Position at dimension {i} must be within the range [{low}, {high}].")

    def _get_best_neighbor(self, fly, dim):
        left_fly = self.flies[fly.left[dim]]
        right_fly = self.flies[fly.right[dim]]
        if self.fitness_function_type == 'min':
            return left_fly if left_fly.fitness < right_fly.fitness else right_fly
        else:  # max
            return left_fly if left_fly.fitness > right_fly.fitness else right_fly
     
    def _update_fly_position(self, fly, d, best_fly):
        # Generate a random number
        rand_num = np.random.rand()
        if rand_num < self.distribution_threshold:
            # Randomly reinitialise the fly's position in the d-th dimension
            fly.position[d] = np.random.uniform(self.dims_range[d][0], self.dims_range[d][1])
        else:
            # Move towards the best fly in the left and right direction in the d-th dimension
            best_neighbor = self._get_best_neighbor(fly, d)
            fly.position[d] = best_neighbor.position[d] + np.random.rand() * (best_fly.position[d] - fly.position[d])

            # Ensure the fly's position is within the bounds of the search space
            fly.position[d] = np.clip(fly.position[d], self.dims_range[d][0], self.dims_range[d][1])
    
    def calculate_fitness(self, position):
        """Calculate the fitness of a given position.

        Args:
            position (list or np.ndarray): The position to evaluate.

        Returns:
            fitness: The fitness value of the given position.
        """
        self._validate_position(position)
        if self.fitness_function is not None:
            return self.fitness_function(position)
        elif self.fitness_matrix is not None:
            try:
                # Convert position to integer indices for accessing the fitness matrix
                indices = tuple(int(pos) for pos in position)
                return self.fitness_matrix[indices]
            except IndexError:
                raise ValueError("Position indices are out of bounds for the fitness matrix.")
        else:
            raise ValueError("No valid fitness evaluation method available.")

    def disperse_flies(self, best_fly):
        """Disperse the flies in the search space based on the best fly.

        Args:
            best_fly: The fly with the best fitness value.
        """
        for fly in self.flies:
            for d in range(len(self.dims_range)):
                self._update_fly_position(fly, d, best_fly)

            # After updating the fly's position, calculate its new fitness
            fly.fitness = self.calculate_fitness(fly.position)

    def get_best_fly(self):
        """Get the best fly with index in the current population.

        Returns:
            best_fly: The fly with the best fitness value.
        """
        if self.fitness_function_type == 'min':
            best_fly = min(self.flies, key=lambda fly: fly.fitness)
        else:  # max
            best_fly = max(self.flies, key=lambda fly: fly.fitness)
        return best_fly

    def optimise(self, best_fly_convergence_holding_iterations: int = None):
        """Run the optimisation process.

        Args:
            best_fly_convergence_holding_iterations (int): The number of iterations to hold the best fly's position for convergence.

        Returns:
            best_fly: The fly with the best fitness value.
        """
        last_best_fly = None
        best_fly_holding_iterations = 0
        best_fly_convergence_holding_iterations = best_fly_convergence_holding_iterations or max(self.max_iterations // 50, 10)  # If not provided, it will never trigger convergence based on holding iterations

        for itr in range(self.max_iterations):
            # Get the best fly in the current population
            best_fly = self.get_best_fly()

            # Check for convergence: If the best fly has been holding its position for a certain number of iterations, we can consider the algorithm to have converged.
            if (
                last_best_fly is not None and 
                best_fly.fitness == last_best_fly.fitness and 
                np.array_equal(best_fly.position, last_best_fly.position)
            ):
                best_fly_holding_iterations += 1
            else:
                best_fly_holding_iterations = 0
            if best_fly_holding_iterations >= best_fly_convergence_holding_iterations:
                logger.info(f"Convergence achieved at iteration {itr}. Best fly has been holding its position for {best_fly_convergence_holding_iterations} iterations.")
                break
            last_best_fly = best_fly

            # Disperse the flies based on the best fly
            self.disperse_flies(best_fly)

        return self.get_best_fly()
    
def test():
    # Example usage of the DFO algorithm
    def sample_fitness_function(position):
        return np.sum(position**2)  # Simple sphere function for testing
    
    # def sample_fitness_function(pos):
    #     # Gaussian function centered at the origin with a standard deviation of 1
    #     return np.exp(-((pos[0]) ** 2 + (pos[1]) ** 2 + (pos[2]) ** 2) / (2 * 5**2))
        
    dims_range = [(-500, 500), (-500, 500), (-500, 500)]  # 3D search space

    dfo = DFO(
        fitness_function=sample_fitness_function,
        dims_range=dims_range,
        num_flies=100,
        max_iterations=1000,
        fitness_function_type='min'
    )
    best_fly = dfo.optimise() #best_fly_convergence_holding_iterations=20)

    logger.info(best_fly)
    # logger.info(dfo.flies)

    logger.info("Best Solution: %s", best_fly.position)
    logger.info("Best Fitness: %s", best_fly.fitness)

if __name__ == "__main__":
    # Example usage of the DFO algorithm
    test()