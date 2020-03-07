import numpy as np


class Setup:

    STARTING_POPULATIONS = ['sp' + str(i) + '.csv' for i in range(1, 50)]
    STARTING_POPULATION_DIR = ''  # TODO fill this directory

    STOP_CONDITIONS = {'maxiter': lambda i, max_i: i >= max_i,
                       'tolfun': lambda val, min_val: val <= min_val}

    @staticmethod
    def generate_starting_population(dim, bounds, filename):
        points = np.random.uniform(low=bounds[0], high=bounds[1], size=(30, dim))
        np.savetxt(filename, points, delimiter=',')

    @staticmethod
    def read_staring_population(filename):
        return np.genfromtxt(filename, delimiter=',')


class EndConditions:

    MAX_ITER = 300

    @staticmethod
    def max_iter(i, max_i):
        return i >= max_i

    @staticmethod
    def tolfun(val1, val2): #TODO Implement this
        return False

    @staticmethod
    def check_end_conditions(iteration, max_iteration, val, min_val):
        return {'max_iter': EndConditions.max_iter(iteration, max_iteration),
                'tolfun': EndConditions.tolfun(val, min_val)}


class Selections:

    @staticmethod
    def tournament_selection(target_fun, x, y):
        if target_fun(x) < target_fun(y):
            return x
        else:
            return y