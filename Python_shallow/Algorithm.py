from General import EndConditions as ec
from General import Setup
import numpy as np
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt

from Point import Point


class Algorithm(ABC):

    def __init__(self, objective_fun, start_pop=None, population_filename=None, plot_data=False):
        super().__init__()
        self.objective_fun = objective_fun  # FUNCTOR

        # You can either use directory to the csv or the numpy array itself
        if start_pop:
            self.population = start_pop  # NUMPY ARRAY OF VECTORS
        elif population_filename:
            self.population = Setup.read_staring_population(
                population_filename)  # READ NUMPY ARRAY FROM CSV
        else:  # Here is my cute defence mechanism for people, who didn't read a documentation
            self.population = np.random.uniform(
                size=(50, np.random.randint(low=1, high=10)))

        self.point_dim = self.population.shape[1]

        # transform multi-d array into numpy array of points
        temp = np.array(
            [Point(coordinates=self.population[i], objective_fun=objective_fun)
             for i in range(len(self.population))]
        )
        self.population = temp

        self.eval_time = -1
        self.iterations = 0  # INT
        self.end_reason = None  # STRING

        # for plotting purposes
        if plot_data:
            plt.ion()
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(111)

    def sel_best(self):
        # create an array of objective function values
        val_array = np.array([p.value for p in self.population])

        # Get the indices of minimum element
        min_index = np.where(val_array == np.amin(val_array))
        # minindex[0][0], because the value returned by np.where is a bit weird
        return self.population[min_index[0][0]]

    def check_end_cond(self, prev_best):
        end_conditions = ec.check_end_conditions(iteration=self.iterations,
                                                 vec1=prev_best, vec2=self.sel_best(),
                                                 obj_fun=self.objective_fun)

        if self.iterations != 0 and any(end_conditions.values()):
            reason = next((i for i, j in enumerate(
                end_conditions.values()) if j), None)
            self.end_reason = list(end_conditions.keys())[reason]
            return True

        else:
            return False

    def update_all_points(self):
        for p in self.population:
            p.update(self.objective_fun)

    def get_population_mean(self):
        pop_matrix = np.array([p.coordinates for p in self.population])
        return pop_matrix.mean(axis=0)

    def plot_population(self):
        if not hasattr(self, 'fig'):
            return
        assert self.point_dim == 2
        x = [point.coordinates[0] for point in self.population]
        y = [point.coordinates[1] for point in self.population]
        self.ax.scatter(x=x, y=y)
        self.fig.canvas.draw_idle()
        plt.pause(0.5)

    @abstractmethod
    def run(self):
        pass
