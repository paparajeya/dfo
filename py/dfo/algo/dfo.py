import logging
from typing import Dict, List, Tuple
import numpy as np

logger = logging.getLogger(__name__)

class DFO:
    def __init__(
        self,
        *,
        fitness_func=None,
        fitness_matrix: np.ndarray = None,
        dims_range: List | Tuple = [200, 300, 250],
        num_flies: int = 100,
        max_iter: int = 20,
        fitness_type: str = "max", # min or max
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
        self.best_fly = self.get_best_fly()

    def __validate_params(
            self, fitness_func, fitness_matrix, dims_range, num_flies, max_iter, fitness_type
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
            
    def get_best_fly(self):
        """Get the best fly in the population based on the fitness type.

        Args:
            fitness_type (str, optional): The type of fitness value to optimize. Defaults to "max".

        Returns:
            dict: The best fly in the population.

        Raises:
            ValueError: If the fitness type is not valid.
        """
        if self.fitness_type.lower() not in ["min", "max"]:
            raise ValueError("fitness_type must be either 'min' or 'max'")
        
        best_fly = None
        if self.fitness_type.lower() == "max":
            best_fly = max(self.flies, key=lambda x: x["fitness"])
        else:
            best_fly = min(self.flies, key=lambda x: x["fitness"])
        return best_fly

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
                pos.append(np.random.randint(self.dims_range[i][0], self.dims_range[i][1]))
            return tuple(pos)

    def run(self):
        ...
