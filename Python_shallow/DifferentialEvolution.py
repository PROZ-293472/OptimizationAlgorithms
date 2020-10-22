from Algorithm import Algorithm
import numpy as np
from numpy.random import random
import matplotlib.pyplot as plt

from Point import Point


class DifferentialEvolution(Algorithm):

    DEFAULT_CR = 0.5
    DEFAULT_F = 0.8

    def __init__(self, objective_fun=None, start_pop=None, population_filename=None, plot_data=False, time_eval=False,
                 f=DEFAULT_F, cr=DEFAULT_CR):
        Algorithm.__init__(self, objective_fun, start_pop,
                           population_filename, plot_data, time_eval)

        self.H = start_pop  # NUMPY ARRAY OF VECTORS
        self.cr = cr  # FLOAT - parameter for crossover
        self.f = f  # FLOAT

    def crossover(self, x, y):
        z = np.empty(x.shape[0])
        for i in range(0, x.shape[0]):
            a = random()
            if a < self.cr:
                z[i] = y[i]
            else:
                z[i] = x[i]
        return z

    def tournament(self, x, y):
        res = self.objective_fun.compare(x, y)
        if res > 0:
            return y
        elif res < 0:
            return x
        else:
            if random() >= 0.5:
                return x
            else:
                return y

    def single_iteration(self):
        print(self.sel_best().value)
        self.plot_population()

        next_population = self.population
        for i in range(0, np.size(self.population, axis=0)):

            # SELECTION - generates a random distinct 3 indexes from <0,mi> and picks corresponding points
            indexes = np.random.choice(
                np.arange(self.population.shape[0]), 3, replace=False)
            r = self.population[indexes[0]]
            d_e = np.array([self.population[indexes[1]],
                            self.population[indexes[2]]])

            # MUTATION and CROSSOVER
            M = r.coordinates + self.f * \
                (d_e[1].coordinates - d_e[0].coordinates)
            O = Point(self.crossover(r.coordinates, M))
            O.update(self.objective_fun)

            self.H = np.append(self.H, O.coordinates)

            next_population[i] = self.tournament(self.population[i], O)

        prev_best = self.sel_best()
        self.population = next_population
        self.iterations += 1
        return prev_best

    def run(self):
        self.iterations = 0
        if not self.is_initialized():
            self.gen_random_population()
        prev_best = self.sel_best()

        mean_time = 0 if self.time_eval else None
        # MAIN LOOP
        while not self.check_end_cond(prev_best):
            if self.time_eval:
                payload = self.evaluate_single_iteration_with_time()
                prev_best = payload['data']
                mean_time += payload['time']
            else:
                prev_best = self.single_iteration()

        if mean_time is not None:
            mean_time = mean_time/self.iterations
        return Algorithm.Result(best_point=prev_best, end_reason=self.end_reason, mean_iteration_time=mean_time)
