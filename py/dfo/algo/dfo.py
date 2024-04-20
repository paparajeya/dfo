# -*- coding: utf-8 -*-
"""Driver Program for Dispersive Fly Optimization (DFO) algorithm.

@Author     : Dr Prashant Aparajeya
                Founder & Director @AISimply Ltd
                Computer Vision Scientist
                London, United Kingdom

@Credits    : Dr. Mohammad Majid al-Rifaie
                Senior Lecturer in Computer Science
                Greenwich University, London, UK
                
@Copyright  : Copyright 2024 - present
@Project    : Dispersive Flies Optimization (DFO) Algorithm
"""

from typing import Dict, List, Tuple
import numpy as np
from dfo.core.logger import logger

class DFO:
    def __init__(
        self,
        *,
        fitness_func=None,
        fitness_matrix: np.ndarray = None,
        dims_range: List | Tuple = [200, 300, 250],
        num_flies: int = 100,
        max_iter: int = 100,
        fitness_type: str = "max",  # min or max
    ):
        self.__validate_params(
            fitness_func, fitness_matrix, dims_range, num_flies, max_iter
        )
        self.fitness_func = fitness_func
        self.fitness_matrix = fitness_matrix
        self.dims_range = dims_range
        self.num_flies = num_flies
        self.max_iter = max_iter
        self.fitness_type = fitness_type
        self.__init__dfo()

    def __init__dfo(self):
        """Initialize the DFO algorithm with the given parameters."""

        self.flies: List[Dict] = self.init_flies()
        self.best_fly_index = self.get_best_fly_index()
        self.find_best_neighbour()

    def __validate_params(
        self,
        fitness_func,
        fitness_matrix,
        dims_range,
        num_flies,
        max_iter,
        fitness_type,
    ):
        """Validate the input parameters for the algorithm

        Args:
            fitness_func (callable): The fitness function to be optimized.
            fitness_matrix (numpy.ndarray): The matrix of fitness values for each fly.
            dims_range (list or tuple): The range of each dimension in the search space.
            num_flies (int): The number of flies in the population.
            max_iter (int): The maximum number of iterations for the algorithm.

        Raises:
            ValueError: If any of the input parameters are invalid.
        """
        if fitness_func is None and (
            fitness_matrix is None or len(fitness_matrix) == 0
        ):
            raise ValueError("Either fitness_func or fitness_matrix must be provided")

        if not isinstance(dims_range, (list, tuple)):
            # If the fitness matrix is provided, the dimensions range is inferred from the matrix
            if fitness_matrix is not None:
                dims_range = fitness_matrix.shape
                logger.warning(
                    f"Dimensions range [{dims_range}] inferred from the fitness matrix"
                )
            else:
                raise ValueError("dims_range must be a list of lists")
        if not isinstance(num_flies, int):
            raise ValueError("num_flies must be an integer")
        if not isinstance(max_iter, int):
            raise ValueError("max_iter must be an integer")
        if fitness_type.lower() not in ["min", "max"]:
            raise ValueError("fitness_type must be either 'min' or 'max'")

    def calculate_fitness(self, pos: List | Tuple = None):
        """Calculate the fitness of a position in the search space.

        Args:
            pos (List or Tuple, optional): The position in the search space. Defaults to None.

        Returns:
            float: The fitness value of the given position.

        Raises:
            ValueError: If the position is not provided or is empty.
            ValueError: If the position is not of the same dimension as the problem.

        """
        if not pos or len(pos) == 0:
            raise ValueError("Position must be provided")

        fitness = None

        try:
            fitness = self.fitness_func(pos)
        except:
            # Calculate fitness using fitness matrix where position is in the N dimensional space and fitness is the value at that position
            if len(pos) != self.num_dim:
                raise ValueError(
                    "Position must be of the same dimension as the problem"
                )
            fitness = self.fitness_matrix[tuple(pos)]
        finally:
            return fitness

    def check_convergence(self):
        """Check if flies have converged to the same position."""
        return len(set([fly["position"] for fly in self.flies])) == 1

    def disperse_flies(self, cut_off: float = 0.01):
        for itr in enumerate(self.flies):
            if itr != self.best_fly_index:
                self.update_fly(itr, cut_off)

    def find_best_neighbour(self):
        """Get the best neighbour fly for each fly in the population."""
        for itr in range(len(self.flies)):
            self.flies[itr]["best_neighbour"] = self.get_best_neighbour_fly_index(itr)

    def get_best_fly_index(self):
        """Get the index of the best fly in the population."""
        if self.fitness_type == "min":
            return min(range(len(self.flies)), key=lambda i: self.flies[i]["fitness"])
        else:
            return max(range(len(self.flies)), key=lambda i: self.flies[i]["fitness"])

    def get_best_neighbour_fly_index(self, fly_index: int) -> int:
        """Get the index of the best neighbour fly for a given fly in the population.

        Args:
            fly_index (int): The index of the fly in the population.

        Returns:
            int: The index of the best neighbour fly for the given fly.
        """
        if self.flies[fly_index - 1]["fitness"] < self.flies[fly_index + 1]["fitness"]:
            return (fly_index - 1) % self.num_flies
        else:
            return (fly_index + 1) % self.num_flies

    def init_flies(self):
        """Initialize the flies in the population with random positions and fitness values.

        Returns:
            list: A list of dictionaries representing the flies in the population. Each dictionary contains the
            position and fitness value of a fly.
        """
        flies = []
        for _ in range(self.num_flies):
            pos: Tuple = self.init_position()
            fitness = self.calculate_fitness(pos)
            flies.append({"position": pos, "fitness": fitness})
        return flies

    def init_position(self) -> Tuple:
        """Initialize a random position within the dimensions range.

        Returns:
            Tuple: A tuple representing the randomly generated position within the dimensions range.
        """
        pos = []
        for i in range(self.num_dim):
            # Generate random integer position within the range of the dimension
            pos.append(np.random.randint(self.dims_range[i]))
        return tuple(pos)

    def update_fly(self, fly_index, cut_off: float = 0.005):
        position = self.flies[fly_index]["position"]
        new_position = []

        for i, pos in enumerate(position):
            # Generate random number
            rand_num = np.random.rand()

            # Update position based on random number and cut-off value
            if rand_num < cut_off:
                new_pos = np.random.randint(self.dims_range[i])
            else:
                best_neighbour_pos = self.flies[
                    self.flies[fly_index]["best_neighbour"]
                ]["position"][i]
                new_pos = int(
                    best_neighbour_pos
                    + np.random.rand()
                    * (self.flies[self.best_fly_index]["position"][i] - pos)
                )

                # Check if the new position is within the dimensions range
                if new_pos < 0:
                    new_pos = 0
                elif new_pos >= self.dims_range[i]:
                    new_pos = self.dims_range[i] - 1

            new_position.append(new_pos)

        self.flies[fly_index]["position"] = tuple(new_position)

    def run(self, max_spots: int = 5, num_defaults_before_stop: int = 3):
        dominant_spots = []
        total_defaults = 0
        while len(dominant_spots) < max_spots:
            num_epochs = 0
            while num_epochs < self.max_iter and not self.check_convergence():
                self.disperse_flies()
                self.best_fly_index = self.get_best_fly()
                self.find_best_neighbour()
                num_epochs += 1
            if not self.check_convergence() or self.flies[self.best_fly_index] in dominant_spots:
                logger.warning(f"Fly {self.flies[self.best_fly_index]} is either not converging or is already in the dominant spots")
                total_defaults += 1
            else:
                total_defaults = 0
                dominant_spots.append(self.flies[self.best_fly_index])

            # Stop if the number of defaults exceeds the threshold
            if total_defaults >= num_defaults_before_stop:
                break
