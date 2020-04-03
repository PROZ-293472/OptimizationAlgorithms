from OptimizationAlgorithms.Python.src.algorithms.Algorithm import Algorithm
import numpy as np

from OptimizationAlgorithms.Python.src.entities.Point import Point


class DifferentialEvolution(Algorithm):

    DEFAULT_CR = 0.5
    DEFAULT_F = 0.8

    def __init__(self, objective_fun, start_pop=None, population_filename=None,
                 f=DEFAULT_F, cr=DEFAULT_CR):
        Algorithm.__init__(self, objective_fun, start_pop, population_filename)

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
        res = self.objective_fun.compare(x, y)
        if res > 0:
            return y
        elif res < 0:
            return x
        else:
            if np.random.random() >= 0.5:
                return x
            else:
                return y


    def run(self):
        self.iterations = 0
        prev_best = self.sel_best()

        # plt.ion()
        # fig = plt.figure()
        # ax = fig.add_subplot(111)

        # MAIN LOOP
        while not self.check_end_cond(prev_best):

            self.update_all_points()
            print(self.sel_best().value)

            # # PLOTTING STUFF
            # x = [self.population[i][0] for i in range(0, self.population.shape[0])]
            # y = [self.population[i][1] for i in range(0, self.population.shape[0])]
            # ax.scatter(x=x, y=y)
            # fig.canvas.draw_idle()
            # plt.pause(0.1)

            next_population = self.population
            for i in range(0, np.size(self.population, axis=0)):

                # SELECTION - generates a random distinct 3 indexes from <0,mi> and picks corresponding points
                indexes = np.random.choice(np.arange(self.population.shape[0]), 3, replace=False)
                r = self.population[indexes[0]]
                d_e = np.array([self.population[indexes[1]], self.population[indexes[2]]])

                # MUTATION and CROSSOVER
                M = r.coordinates + self.f * (d_e[1].coordinates - d_e[0].coordinates)
                O = Point(self.crossover(r.coordinates, M))
                O.update(self.objective_fun)

                self.H = np.append(self.H, O.coordinates)

                next_population[i] = self.tournament(self.population[i], O)

            prev_best = self.sel_best()
            self.population = next_population
            self.iterations += 1







