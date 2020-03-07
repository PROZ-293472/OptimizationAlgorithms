from OptimizationAlgorithms.Python.src.General  import EndConditions as ec
from OptimizationAlgorithms.Python.src.General import Setup
import numpy as np
import matplotlib.pyplot as plt


class DifferentialEvolution:

    DEFAULT_CR = 0.5
    DEFAULT_F = 0.8

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
        self.max_iterations = max_iter  # INT
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
        return self.population[min_index[0][0]]  # minindex[0][0], because the value returned by np.where is a bit weird

    def run(self):
        self.iterations = 0

        plt.ion()
        fig = plt.figure()
        ax = fig.add_subplot(111)

        while not any([cond for cond in ec.check_end_conditions(self.iterations, self.max_iterations, 0, 1).values()]):
            print(self.target_fun(self.sel_best()))
            # # DEBUG PURPOSES
            x = [self.population[i][0] for i in range(0, self.population.shape[0])]
            y = [self.population[i][1] for i in range(0, self.population.shape[0])]

            ax.scatter(x=x, y=y)

            fig.canvas.draw_idle()
            plt.pause(0.1)

            temp_population = self.population
            for i in range(0, np.size(self.population, axis=0)):

                # SELECTION - generates a random distinct 3 indexes from <0,mi> and picks corresponding vectors
                indexes = np.random.choice(np.arange(self.population.shape[0]), 3, replace=False)
                r = self.population[indexes[0]]
                d_e = np.array([self.population[indexes[1]], self.population[indexes[2]]])

                # MUTATION and CROSSOVER
                M = r + self.f * (d_e[1] - d_e[0])
                O = self.crossover(r, M)

                self.H = np.append(self.H, O)

                temp_population[i] = self.tournament(self.population[i], O)

            self.population = temp_population
            self.iterations += 1







