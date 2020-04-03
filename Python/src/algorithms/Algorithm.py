from OptimizationAlgorithms.Python.src.General  import EndConditions as ec
from OptimizationAlgorithms.Python.src.General import Setup
import numpy as np
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt


class Algorithm(ABC):

    def __init__(self, objective_fun, start_pop=None, population_filename=None):
        super().__init__()
        self.objective_fun = objective_fun  # FUNCTOR

        # You can either use directory to the csv or the numpy array itself
        if start_pop:
            self.population = start_pop  # NUMPY ARRAY OF VECTORS
        elif population_filename:
            self.population = Setup.read_staring_population(population_filename)  # READ NUMPY ARRAY FROM CSV
        else:  # Here is my cute defence mechanism for people, who didn't read a documentation
            self.population = np.random.uniform(size=(50, np.random.randint(low=1, high=10)))
        self.eval_time = -1
        self.iterations = 0  # INT
        self.end_reason = None  # STRING

    def sel_best(self):
        # create an array of target function values
        val_array = np.array([self.objective_fun.eval(i) for i in self.population])

        # Get the indices of minimum element
        min_index = np.where(val_array == np.amin(val_array))
        return self.population[min_index[0][0]]  # minindex[0][0], because the value returned by np.where is a bit weird

    def check_end_cond(self, prev_best):
        end_conditions = ec.check_end_conditions(iteration=self.iterations,
                                                 vec1=prev_best, vec2=self.sel_best(),
                                                 obj_fun=self.objective_fun)

        if self.iterations != 0 and any(end_conditions.values()):
            reason = next((i for i, j in enumerate(end_conditions.values()) if j), None)
            self.end_reason = list(end_conditions.keys())[reason]
            return True

        else:
            return False

    @abstractmethod
    def run(self):
        pass

