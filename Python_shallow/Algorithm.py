import time
import numpy as np
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from collections import namedtuple

from General import EndConditions as ec
from General import Setup
from Point import Point


class Algorithm(ABC):
    Result = namedtuple(
        'Result', ['best_point', 'end_reason', 'mean_iteration_time'])

    def __init__(self, objective_fun=None, start_pop=None, population_filename=None, plot_data=False, time_eval=False, max_iter=ec.MAX_ITER):
        super().__init__()
        self.objective_fun = objective_fun  # FUNCTOR

        # You can either use directory to the csv or the numpy array itself
        if start_pop:
            self.population = start_pop  # NUMPY ARRAY OF VECTORS
        elif population_filename:
            self.population = Setup.read_staring_population(
                population_filename)  # READ NUMPY ARRAY FROM CSV
        else:
            self.population = None

        if self.population:
            self.point_dim = self.population.shape[1]
            # transform multi-d array into numpy array of points
            temp = np.array(
                [Point(coordinates=self.population[i], objective_fun=objective_fun)
                 for i in range(len(self.population))]
            )
            self.population = temp
        elif self.objective_fun:
            self.point_dim = self.objective_fun.dim
        else:
            self.point_dim = None

        self.eval_time = -1
        self.iterations = 0  # INT
        self.max_iter = max_iter
        self.end_reason = None  # STRING

        # for plotting purposes
        if plot_data:
            self.enable_plotting()

    def is_initialized(self, valid_parameters=None):
        if valid_parameters:
            parameter_list = [p for key, p in enumerate(
                self.__dict__.values()) if key in valid_parameters]
        else:
            parameter_list = self.__dict__.values()

        for val in parameter_list:
            if val is None:
                return False
        return True

    def enable_plotting(self):
        plt.ion()
        setattr(self, 'fig', plt.figure())
        setattr(self, 'ax', self.fig.add_subplot(111))

    def set_obj_function(self, objective_fun):
        self.objective_fun = objective_fun
        self.point_dim = objective_fun.dim
        if self.population and self.population.shape[1] != self.point_dim:
            self.population = None

    def set_parameters(self, parameter_dict):
        for key in parameter_dict:
            if key in self.__dict__.keys():
                setattr(self, key, parameter_dict[key])

    def gen_random_population(self, size=50, scaler=1):
        generated = scaler * \
            np.random.uniform(size=(size, np.random.randint(
                low=self.point_dim, high=self.point_dim+1)))
        raw_population = np.array([Point(
            coordinates=generated[i], objective_fun=self.objective_fun) for i in range(len(generated))])

        if self.objective_fun.bounds:
            self.population = self.objective_fun.repair_points(raw_population)

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
                                                 obj_fun=self.objective_fun, max_iter=self.max_iter)

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

    def evaluate_single_iteration_with_time(self, *args):
        start_time = time.time()
        out = self.single_iteration(*args)
        return {'data': out, 'time': time.time() - start_time}

    @abstractmethod
    def single_iteration(self):
        pass

    @abstractmethod
    def run(self):
        pass
