import math

from OptimizationAlgorithms.Python.src.algorithms.Algorithm import Algorithm
import numpy as np

from OptimizationAlgorithms.Python.src.entities.Point import Point


class CMAES(Algorithm):

    DEFAULT_SIGMA = 1
    DEFAULT_LAMBDA = 50

    def __init__(self, objective_fun, start_pop=None,
                 population_filename=None, sigma=DEFAULT_SIGMA, lmbd=DEFAULT_LAMBDA):

        Algorithm.__init__(self, objective_fun, start_pop, population_filename)
        self.C = np.eye(N=self.point_dim, dtype=int)
        self.sigma = sigma
        self.lmbd = lmbd

    def generate_di(self, lbd):
        mean = np.zeros(self.point_dim)
        di = np.random.multivariate_normal(mean, self.C, lbd)
        # returns numpy array of vectors
        return di

    def run(self):
        self.iterations = 0
        prev_best = self.sel_best()
        m = self.get_population_mean()
        p_c = 0
        p_sgm = 0

        # plt.ion()
        # fig = plt.figure()
        # ax = fig.add_subplot(111)

        # MAIN LOOP
        while not self.check_end_cond(prev_best):

            di = self.generate_di(self.lmbd)
            coords = m + self.sigma * di
            qi = [Point(coordinates=i, objective_fun=self.objective_fun) for i in coords]
            qi_vals = np.array([q.value for q in qi])

            # sort by qi_vals
            index_order = qi_vals.argsort()
            di = di[index_order[::-1]]

            mi = math.floor(len(di) / 2)
            d_t = (1/mi) * np.sum(di[0:mi], axis=0)

            m = m + self.sigma * d_t

            next_p_s =
            next_p_sgm =

            self.iterations += 1


