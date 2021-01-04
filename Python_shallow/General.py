import numpy as np
import time
import math


class Setup:

    STARTING_POPULATIONS = [f'sp{str(i)}.csv' for i in range(1, 50)]
    STARTING_POPULATION_DIR = ''  # TODO fill this directory

    STOP_CONDITIONS = {'maxiter': lambda i, max_i: i >= max_i,
                       'tolfun': lambda val, min_val: val <= min_val}

    @staticmethod
    def generate_starting_population(pop_size, dim, bounds, filename):
        points = np.random.uniform(
            low=bounds[0], high=bounds[1], size=(pop_size, dim))
        np.savetxt(filename, points, delimiter=',')

    @staticmethod
    def read_staring_population(filename):
        return np.genfromtxt(filename, delimiter=',')


class EndConditions:

    MAX_ITER = 10e6
    TOLERANCE = 0
    TOL_FUN = 0.0000001

    @staticmethod
    def max_iter(i, max_iter):
        return i >= max_iter

    @staticmethod
    def tol_fun(vec1, vec2, objective_fun):
        return False

    @staticmethod
    def tol(vec, tolerance):
        return vec.value <= tolerance

    @staticmethod
    def check_end_conditions(iteration, vec1, vec2, obj_fun, max_iter, tol):
        return {'max_iter': EndConditions.max_iter(iteration, max_iter),
                'tolfun': EndConditions.tol_fun(vec1=vec1, vec2=vec2, objective_fun=obj_fun),
                'tolerance': EndConditions.tol(vec=vec2, tolerance=tol)}


class Selections:

    @staticmethod
    def tournament_selection(target_fun, x, y):
        if target_fun(x) < target_fun(y):
            return x
        else:
            return y


class Utils:

    @staticmethod
    def time_evaluation(function, **kwargs):
        start_time = time.time()
        function(**kwargs)
        return time.time() - start_time
