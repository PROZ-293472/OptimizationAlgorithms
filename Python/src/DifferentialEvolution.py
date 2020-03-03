from OptimizationAlgorithms.Python.src.General  import EndConditions as ec
from OptimizationAlgorithms.Python.src.General import Setup
import numpy as np


class DifferentialEvolution:

    DEFAULT_CR = 0.2
    DEFAULT_F = 0.2

    def __init__(self, target_fun, start_pop=None, population_filename=None,
                 f=DEFAULT_F, cr=DEFAULT_CR, max_iter=ec.MAX_ITER):
        self.target_fun = target_fun  # FUNCTOR

        # You can either use directory to the csv or the numpy array itself
        if start_pop:
            self.population = start_pop  # NUMPY ARRAY OF VECTORS
        elif population_filename:
            self.population = Setup.read_staring_population(population_filename)  # READ NUMPY ARRAY FROM CSV
        else:  # Here is my cute defence mechanism for people, who didn't read a documentation
            self.population = np.random.uniform(size=(50, np.random.randint(low=1, high=10)))

        self.H = start_pop  # NUMPY ARRAY OF VECTORS
        self.cr = cr  # FLOAT - parameter for crossover
        self.f = f  # FLOAT
        self.eval_time = -1
        self.iterations = 0  # INT
        self.max_iterations = max_iter # INT
        self.end_reason = None  # STRING

    def crossover(self, x, y):
        z = np.empty(x.shape[0])
        for i in range(0, x.shape[0]):
            a = np.random.random()
            if a < self.cr:
                z[i] = y[i]
            else:
                z[i] = x[i]
        return z

    def tournament(self, x, y):
        if self.target_fun(x) < self.target_fun(y):
            return x
        else:
            return y

    def sel_best(self):
        # create an array of target function values
        val_array = np.array([self.target_fun(i) for i in self.population])

        # Get the indices of minimum element
        min_index = np.where(val_array == np.amin(val_array))
        return self.population[min_index]

    def run(self):
        self.iterations = 0
        while not any([cond for cond in ec.check_end_conditions(self.iterations, self.max_iterations, 0, 1).values()]):
            print(self.population)
            for i in range(0, np.size(self.population, axis=0)):

                # SELECTION - generates a random index from <0,mi> and picks corresponding vector
                r = self.population[np.random.choice(np.size(self.population, axis=0))]
                # SELECTION pt 2 - two random d i s t i n c t points
                d_e = self.population[np.random.choice(np.size(self.population, axis=0), 2, replace=False)]

                M = r + self.f * (d_e[1] - d_e[0])
                O = self.crossover(r, M)

                self.H = np.append(self.H, O)

                self.population[i] = self.tournament(self.population[i], O)

            self.iterations += 1






