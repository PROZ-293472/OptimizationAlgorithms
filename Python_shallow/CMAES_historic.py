import math
import numpy as np
import scipy as sp
import scipy.special
import matplotlib.pyplot as plt

from Algorithm import Algorithm
from Point import Point

# TODO: Przepatrz kod i porownaj z algorytmem, bo sigma dazy do nieskonczonosci


class CMAES(Algorithm):

    DEFAULT_SIGMA = 1
    DEFAULT_LAMBDA = 50
    DEFAULT_CC = 0.5
    DEFAULT_DSIGM = 1
    MAX_SIGMA = 1000000

    def __init__(self, objective_fun, start_pop=None, population_filename=None, plot_data=False,
                 sigma=DEFAULT_SIGMA, lmbd=DEFAULT_LAMBDA, cc=None, csigm=None, dsigm=DEFAULT_DSIGM,
                 learning_rate_1=None, learning_rate_mu=None):

        Algorithm.__init__(self, objective_fun, start_pop,
                           population_filename, plot_data)
        self.C = np.eye(N=self.point_dim, dtype=int)
        self.sigma = sigma
        self.lmbd = lmbd
        if not cc:
            self.cc = 4 / self.point_dim
        else:
            self.cc = cc

        if not csigm:
            self.csigm = 3 / self.point_dim
        else:
            self.csigm = csigm

        self.dsigm = dsigm

        if not learning_rate_1:
            self.learning_rate_1 = 2 / self.point_dim ** 2
        else:
            self.learning_rate_1 = learning_rate_1

        if not learning_rate_mu:
            self.learning_rate_mu = 4 / self.lmbd
        else:
            self.learning_rate_mu = learning_rate_mu

    def generate_di(self, lbd):
        mean = np.zeros(self.point_dim)
        di = np.random.multivariate_normal(mean, self.C, lbd)
        # returns numpy array of vectors
        return di

    def run(self):
        self.iterations = 0
        prev_best = self.sel_best()
        p_c = np.zeros(self.point_dim)
        p_sgm = np.zeros(self.point_dim)
        m = self.get_population_mean()
        # formula for the mean of the chi distribution ...idk
        chi_mean = math.sqrt(2) * scipy.special.gamma((self.point_dim +
                                                       1)/2) / scipy.special.gamma(self.point_dim/2)

        # MAIN LOOP
        while not self.check_end_cond(prev_best):

            self.plot_population()
            print(self.sel_best().value)

            di = self.generate_di(self.lmbd)
            coords = m + self.sigma * di
            qi = np.array(
                [Point(coordinates=i, objective_fun=self.objective_fun) for i in coords])
            qi_vals = np.array([q.value for q in qi])

            # sort by qi_vals
            index_order = qi_vals.argsort()
            di = di[index_order[::1]]

            mi = math.floor(len(di) / 2)
            d_t = (1/mi) * np.sum(di[0:mi], axis=0)

            next_m = m + self.sigma * d_t
            fact_C = sp.linalg.sqrtm(np.linalg.inv(self.C))
            next_p_sgm = (1 - self.csigm)*p_sgm + fact_C * \
                math.sqrt(1 - (1 - self.csigm)**2) * math.sqrt(mi)*d_t
            next_p_c = (1-self.cc)*p_c + math.sqrt(1 -
                                                   (1 - self.cc)**2) * math.sqrt(mi)*d_t

            try:
                next_sigma = self.sigma * \
                    math.exp(self.csigm/self.dsigm *
                             (np.linalg.norm(p_sgm)/chi_mean - 1))
                if next_sigma > CMAES.MAX_SIGMA:
                    next_sigma = CMAES.MAX_SIGMA
            except OverflowError:
                next_sigma = CMAES.MAX_SIGMA

            d_sum = 0
            for i in range(mi):
                d_sum += di[i] * np.transpose(di[i])

            next_C = (1 - self.learning_rate_1 - self.learning_rate_mu)*self.C + \
                self.learning_rate_1 * next_p_c * \
                np.transpose(next_p_c) + self.learning_rate_mu * d_sum

            self.sigma = next_sigma
            self.population = qi
            self.C = next_C
            p_c = next_p_c
            p_sgm = next_p_sgm
            self.iterations += 1
            m = next_m
