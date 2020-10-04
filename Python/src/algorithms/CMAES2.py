import math
import numpy as np
import scipy as sp
import scipy.special
import matplotlib.pyplot as plt

from Algorithm import Algorithm
from Point import Point

# TODO: Przepatrz kod i porownaj z algorytmem, bo sigma dazy do nieskonczonosci


class CMAES2(Algorithm):

    DEFAULT_SIGMA = 1
    DEFAULT_LAMBDA = 50
    DEFAULT_CC = 0.5
    DEFAULT_DSIGM = 1
    MAX_SIGMA = 1000000

    def __init__(self, objective_fun, start_pop=None, population_filename=None, plot_data=False,
                 sigma=DEFAULT_SIGMA, lmbd=DEFAULT_LAMBDA):

        Algorithm.__init__(self, objective_fun, start_pop,
                           population_filename, plot_data)
        self.C = np.eye(N=self.point_dim, dtype=int)
        self.sigma = sigma
        self.lmbd = lmbd
        self.p_sgm = np.zeros(self.point_dim)
        self.p_c = np.zeros(self.point_dim)
        self.m = self.get_population_mean()

    # def generate_di(self, lbd):
    #     mean = np.zeros(self.point_dim)
    #     di = np.random.multivariate_normal(mean, self.C, lbd)
    #     # returns numpy array of vectors
    #     return di

    def generate_samples(self):
        samples = np.random.multivariate_normal(
            self.m, self.C * self.sigma**2, self.lmbd)
        return samples

    def run(self):
        self.iterations = 0

        prev_best = self.sel_best()
        while not self.check_end_cond(prev_best=prev_best):
            samples = self.generate_samples()
