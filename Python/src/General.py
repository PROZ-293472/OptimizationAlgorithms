import numpy as np


class Setup:

    STARTING_POPULATIONS = ['sp' + str(i) + '.csv' for i in range(1, 50)]
    STARTING_POPULATION_DIR = ''  # TODO fill this directory

    STOP_CONDITIONS = {'maxiter': lambda i, max_i: i >= max_i,
                       'tolfun': lambda val, min_val: val <= min_val}

    @staticmethod
    def generate_starting_population(pop_size, dim, bounds, filename):
        points = np.random.uniform(low=bounds[0], high=bounds[1], size=(pop_size, dim))
        np.savetxt(filename, points, delimiter=',')

    @staticmethod
    def read_staring_population(filename):
        return np.genfromtxt(filename, delimiter=',')


class EndConditions:

    MAX_ITER = 400
    TOL_X = 0.0000001
    TOL_FUN = 0.0000001

    @staticmethod
    def max_iter(i):
        return i >= EndConditions.MAX_ITER

    @staticmethod
    def tol_fun(vec1, vec2, objective_fun):
        return False

    @staticmethod
    def tol_x(vec1, vec2):
        return False

    @staticmethod
    def check_end_conditions(iteration, vec1, vec2, obj_fun):
        return {'max_iter': EndConditions.max_iter(iteration),
                'tolfun': EndConditions.tol_fun(vec1=vec1, vec2=vec2, objective_fun=obj_fun),
                'tolx': EndConditions.tol_x(vec1=vec1, vec2=vec2)}


class Selections:

    @staticmethod
    def tournament_selection(target_fun, x, y):
        if target_fun(x) < target_fun(y):
            return x
        else:
            return y