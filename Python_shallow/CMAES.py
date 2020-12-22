import math
import numpy as np
from numpy import random
import numpy.matlib as matlib
from Algorithm import Algorithm
from Point import Point

from memory_profiler import profile


class CMAES(Algorithm):

    DEFAULT_SIGMA = 0.3

    def __init__(self, objective_fun=None, start_pop=None, population_filename=None, plot_data=False, time_eval=False,
                 sigma=DEFAULT_SIGMA, lbd=None, mean=None):

        Algorithm.__init__(self, objective_fun, start_pop,
                           population_filename, plot_data, time_eval)

        self.sigma = sigma
        self.m = mean
        self.lbd = lbd
        self.mu = None
        self.weights = None
        self.mu_w = None
        self.cc = None
        self.cs = None
        self.c1 = None
        self.cmu = None
        self.d_s = None
        self.chiN = None
        if self.population and self.point_dim:
            self.init_default_parameters()

    def init_default_parameters(self):
        if not self.m:  # staring mean point
            self.m = self.get_population_mean()

        if not self.lbd:
            self.lbd = len(self.population)

        mu = self.lbd/2   # offsprings number
        if not self.mu:
            self.mu = math.floor(mu)

        weights = math.log(mu + 1/2) - \
            np.array([math.log(i)
                      for i in range(1, self.mu)])  # initialized weights
        if not self.weights:
            self.weights = weights/np.sum(weights)  # weight normalised

        if not self.mu_w:
            self.mu_w = np.sum(self.weights**2)**(-1)

        if not self.cc:
            self.cc = (4 + self.mu_w/self.point_dim) / \
                (self.point_dim + 4 + 2*self.mu_w/self.point_dim)
        if not self.cs:
            self.cs = (self.mu_w + 2) / (self.point_dim + self.mu_w+5)
        if not self.c1:
            self.c1 = 2 / ((self.point_dim + 1.3)**2 + self.mu_w)
        if not self.cmu:
            self.cmu = min(1-self.c1, 2 * (self.mu_w-2 +
                                           1/self.mu_w) / ((self.point_dim + 2)**2 + self.mu_w))
        if not self.d_s:
            self.d_s = 1 + 2 * \
                max(0, math.sqrt((self.mu_w - 1)/(self.point_dim + 1)) - 1) + self.cs
        if not self.chiN:
            self.chiN = self.point_dim**0.5 * \
                (1-1/(4*self.point_dim)+1/(21*self.point_dim**2))

    def generate_population(self, C):
        generated_pop = self.m + self.sigma * \
            np.random.multivariate_normal(
                np.zeros(self.point_dim), C, self.lbd)
        points = np.array(
            [Point(coordinates=i, objective_fun=self.objective_fun) for i in generated_pop])
        if self.objective_fun.bounds:
            points_repaired = self.objective_fun.repair_points(points)
            return points_repaired
        return points
        # print(points == points_repaired)
        # print(len(points))
        # print(len(points_repaired))

    def sort_by_fitness(self, population):
        fitnesses = np.array([p.value for p in population])
        index_order = [int(i) for i in fitnesses.argsort()]
        pop_sorted = [population[i] for i in index_order]
        return pop_sorted

    def update_cov_matrix(self, C, pop_sorted_coordinates, pc, ps, flag_sigma):
        artmp = (1/self.sigma) * \
            (pop_sorted_coordinates.T[:, 0:self.mu-1] -
             matlib.repmat(self.m, self.mu-1, 1).T)
        try:
            C = (1-self.c1-self.cmu) * C + self.c1*(pc @ pc.T + (1-flag_sigma)*self.cc *
                                                    (2-self.cc)*C) + self.cmu * artmp @ np.diag(self.weights) @ artmp.T
            self.sigma = self.sigma * \
                math.exp((self.cs/self.d_s) *
                         (np.linalg.norm(ps)/self.chiN - 1))
            C = np.triu(C) + np.triu(C, 1).T
            w, v = np.linalg.eig(C)
            temp = []
            for d in w:
                if d < 0:
                    temp.append(0)
                else:
                    temp.append(math.sqrt(d)**(-1))
            w = np.array(temp)
            C_fact = v @ np.diag(w) @ v.T
        except ZeroDivisionError:
            C = np.eye(self.point_dim)
            C_fact = np.eye(self.point_dim)
        return C, C_fact

    # @profile
    def single_iteration(self, C, C_fact, pc, ps, prev_best):
        # GENERATE NEW POPULATION
        self.population = self.generate_population(C)

        self.plot_population()
        best_point = self.sel_best()
        # print(best_point.value)

        # SORT BY FITNESS AND GET A COORDINATE MATRIX
        pop_sorted = self.sort_by_fitness(self.population)
        pop_sorted_coordinates = np.array(
            [p.coordinates for p in pop_sorted])

        # GET NEW MEAN OF POPULATION
        new_m = pop_sorted_coordinates.T[:, 0:self.mu-1] @ self.weights

        # UPDATE EVOLUTION PATHS
        ps = (1-self.cs)*ps + math.sqrt(self.cs*(2-self.cs) *
                                        self.mu_w) * C_fact @ (new_m-self.m) / self.sigma
        HIGH_SIGMA = np.linalg.norm(
            ps)/math.sqrt(1-(1-self.cs)**(2*self.iterations/self.lbd))/self.chiN < 1.4 + 2/(self.point_dim+1)
        pc = (1-self.cc)*pc + HIGH_SIGMA * math.sqrt(self.cc *
                                                     (2-self.cc)*self.mu_w) * (new_m-self.m) / self.sigma

        # UPDATE COVARIANCE MATRIX
        C, C_fact = self.update_cov_matrix(
            C, pop_sorted_coordinates, pc, ps, HIGH_SIGMA)

        # ASSIGN NEW VALUES TO SOME PARAMETERS
        self.m = new_m
        prev_best = best_point
        self.iterations += 1
        return C, C_fact, pc, ps, prev_best

    def run(self):
        assert self.point_dim is not None
        if self.population is None:
            self.gen_random_population()
        if not self.is_initialized():
            self.init_default_parameters()

        self.iterations = 0
        C = np.eye(self.point_dim)
        C_fact = np.eye(self.point_dim)
        pc = np.zeros(self.point_dim)
        ps = np.zeros(self.point_dim)
        self.iterations = 0
        prev_best = self.sel_best()

        mean_time = 0 if self.time_eval else None

        while not self.check_end_cond(prev_best=prev_best):
            try:
                if self.time_eval:
                    payload = self.evaluate_single_iteration_with_time(
                        C, C_fact, pc, ps, prev_best)
                    C, C_fact, pc, ps, best = payload['data']
                    mean_time += payload['time']
                else:
                    C, C_fact, pc, ps, best = self.single_iteration(
                        C, C_fact, pc, ps, prev_best)
            except ArithmeticError:
                break
            if prev_best.value >= best.value:
                prev_best = best

        if mean_time is not None:
            mean_time = mean_time/self.iterations
        return Algorithm.Result(best_point=prev_best, end_reason=self.end_reason, mean_iteration_time=mean_time)
