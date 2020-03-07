from OptimizationAlgorithms.Python.src.Algorithm import Algorithm
from OptimizationAlgorithms.Python.src.General  import EndConditions as ec
from OptimizationAlgorithms.Python.src.General import Setup
import numpy as np
import matplotlib.pyplot as plt


class DifferentialEvolution(Algorithm):

    DEFAULT_CR = 0.5
    DEFAULT_F = 0.8

    def __init__(self, target_fun, start_pop=None, population_filename=None,
                 f=DEFAULT_F, cr=DEFAULT_CR):
        Algorithm.__init__(self, target_fun, start_pop, population_filename)

        self.H = start_pop  # NUMPY ARRAY OF VECTORS
        self.cr = cr  # FLOAT - parameter for crossover
        self.f = f  # FLOAT


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

    def run(self):
        self.iterations = 0
        prev_best = self.sel_best()

        plt.ion()
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # MAIN LOOP
        while True:
            # CHECKING ENDING CONDITIONS
            end_conditions = ec.check_end_conditions(iteration=self.iterations,
                                                     vec1=prev_best, vec2=self.sel_best(),
                                                     target_fun=self.target_fun)

            if self.iterations != 0 and any(end_conditions.values()):
                reason = next((i for i, j in enumerate(end_conditions.values()) if j), None)
                self.end_reason = list(end_conditions.keys())[reason]
                break

            print(self.target_fun(self.sel_best()))

            # PLOTTING STUFF
            x = [self.population[i][0] for i in range(0, self.population.shape[0])]
            y = [self.population[i][1] for i in range(0, self.population.shape[0])]
            ax.scatter(x=x, y=y)
            fig.canvas.draw_idle()
            plt.pause(0.1)

            next_population = self.population
            for i in range(0, np.size(self.population, axis=0)):

                # SELECTION - generates a random distinct 3 indexes from <0,mi> and picks corresponding vectors
                indexes = np.random.choice(np.arange(self.population.shape[0]), 3, replace=False)
                r = self.population[indexes[0]]
                d_e = np.array([self.population[indexes[1]], self.population[indexes[2]]])

                # MUTATION and CROSSOVER
                M = r + self.f * (d_e[1] - d_e[0])
                O = self.crossover(r, M)

                self.H = np.append(self.H, O)

                next_population[i] = self.tournament(self.population[i], O)

            prev_best = self.sel_best()
            self.population = next_population
            self.iterations += 1







