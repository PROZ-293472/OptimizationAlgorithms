from Algorithm import Algorithm
from Point import Point
import math
import numpy as np


class DES(Algorithm):

    def __init__(self, objective_fun=None, start_pop=None, population_filename=None, plot_data=False, time_eval=False,
                 mean=None, lbd=None, hist_size=None, path_len=None):

        Algorithm.__init__(self, objective_fun, start_pop,
                           population_filename, plot_data, time_eval)
        self.m = mean
        self.lbd = lbd
        # if lbd:
        #     self.lbd = lbd
        # else:
        #     self.lbd = 4*self.point_dim
        self.mu = None
        self.weights = None
        self.weights_pop = None
        self.mu_eff = None
        self.cc = None
        self.cp = None
        self.Ft = None
        self.c_Ft = None
        self.path_len = path_len
        self.path_ratio = None
        self.hist_size = hist_size
        if self.population and self.point_dim:
            self.init_default_parameters()

    def init_default_parameters(self):
        if not self.m:
            self.m = self.get_population_mean()
        if not self.lbd:
            self.lbd = len(self.population)
            # self.lbd = 4*self.point_dim
        if not self.mu:
            self.mu = math.floor(self.lbd/2)
        if not self.weights:
            temp = np.array([math.log(self.mu+1) - math.log(i)
                             for i in range(1, self.mu+1)])
            self.weights = temp/np.sum(temp)
        if not self.weights_pop:
            temp = np.array([math.log(self.lbd+1) - math.log(i)
                             for i in range(1, self.lbd+1)])
            self.weights_pop = temp/np.sum(temp)
        if not self.mu_eff:
            self.mu_eff = np.sum(self.weights)**2/np.sum(self.weights**2)
        if not self.cc:
            self.cc = self.mu/(self.mu + 2)
        if not self.cp:
            self.cp = 1/math.sqrt(self.point_dim)
        if not self.Ft:
            self.Ft = 1
        if not self.c_Ft:
            self.c_Ft = 0
        if not self.path_len:
            self.path_len = 6
        if not self.path_ratio:
            self.path_ratio = math.sqrt(self.path_len)
        if not self.hist_size:
            self.hist_size = math.ceil(
                6 + math.ceil(3*math.sqrt(self.point_dim)))

    @staticmethod
    def sort_by_fitness(population):
        fitnesses = np.array([p.value for p in population])
        index_order = [int(i) for i in fitnesses.argsort()]
        pop_sorted = [population[i] for i in index_order]
        return pop_sorted

    def selection(self, population):
        pop_sorted = DES.sort_by_fitness(population)
        return pop_sorted[:self.mu]

    def single_iteration(self, history, hist_norm, pop_mean, d_mean, pc, diffs):
        self.plot_population()
        best_point = self.sel_best()
        # print(best_point.value)

        hist_iterator = self.iterations % self.hist_size
        selected_points = self.selection(self.population)
        selected_points_mat = np.array(
            [p.coordinates for p in selected_points]).T

        history[hist_iterator] = selected_points_mat * hist_norm/self.Ft

        new_m = selected_points_mat @ self.weights
        d_mean[:, hist_iterator] = (new_m - pop_mean) / self.Ft

        step = (new_m - self.m) / self.Ft

        if hist_iterator == 0:
            pc[:, hist_iterator] = (1-self.cp) * np.zeros(self.point_dim)/math.sqrt(
                self.point_dim) + math.sqrt(self.mu*self.cp*(2-self.cp))*step
        else:
            pc[:, hist_iterator] = (
                1-self.cp) * pc[:, hist_iterator-1] + math.sqrt(self.mu*self.cp*(2-self.cp))*step

        limit = min(self.iterations, self.hist_size-1)

        history_sample_1 = np.random.choice(
            list(range(limit+1)), size=self.lbd)
        history_sample_2 = np.random.choice(
            list(range(limit+1)), size=self.lbd)

        x1_sample = np.random.choice(list(range(self.mu)), size=self.lbd)
        x2_sample = np.random.choice(list(range(self.mu)), size=self.lbd)

        for i in range(self.lbd):
            x1 = history[history_sample_1[i]][:, x1_sample[i]]
            x2 = history[history_sample_1[i]][:, x2_sample[i]]

            diffs[:, i] = math.sqrt(self.cc)*((x1-x2) + np.random.normal(size=1)*d_mean[:, history_sample_1[i]]
                                              ) + math.sqrt(1-self.cc) * np.random.normal(size=1)*pc[:, history_sample_2[i]]

        new_population_mat = new_m + self.Ft * diffs.T
        pop_mean = new_population_mat.T @ self.weights_pop

        new_population = [Point(coordinates=c, objective_fun=self.objective_fun)
                          for c in new_population_mat]

        prev_best = best_point
        self.population = new_population
        if self.objective_fun.bounds:
            self.population = self.objective_fun.repair_points(self.population)
        self.m = new_m

        self.iterations += 1

        return history, hist_norm, pop_mean, d_mean, pc, diffs, prev_best

    def run(self):
        assert self.point_dim is not None
        self.lbd = 4*self.point_dim
        if self.population is None and not self.lbd:
            self.gen_random_population()
        elif self.population is None and self.lbd:
            self.gen_random_population(size=self.lbd)
        if not self.is_initialized():
            self.init_default_parameters()

        d_mean = np.zeros(shape=(self.point_dim, self.hist_size))
        pc = np.zeros(shape=(self.point_dim, self.hist_size))
        history = [None]*self.hist_size
        diffs = np.zeros(shape=(self.point_dim, self.lbd))

        pop_coordinates = np.array([p.coordinates for p in self.population])
        pop_mean = pop_coordinates.T @ self.weights_pop

        hist_norm = 1/math.sqrt(2)

        prev_best = self.sel_best()
        mean_time = 0 if self.time_eval else None
        times_list = []
        self.iterations = 0

        while not self.check_end_cond(prev_best=prev_best):
            try:
                if self.time_eval:
                    payload = self.evaluate_single_iteration_with_time(
                        history, hist_norm, pop_mean, d_mean, pc, diffs)
                    history, hist_norm, pop_mean, d_mean, pc, diffs, best = payload['data']
                    mean_time += payload['time']
                    times_list.append(payload['time'])
                else:
                    history, hist_norm, pop_mean, d_mean, pc, diffs, best = self.single_iteration(
                        history, hist_norm, pop_mean, d_mean, pc, diffs)
            except ArithmeticError:
                break
            if prev_best.value >= best.value:
                prev_best = best

        if mean_time is not None:
            mean_time = mean_time/self.iterations
        return Algorithm.Result(best_point=self.sel_best(), end_reason=self.end_reason, mean_iteration_time=mean_time, iteration_num=self.iterations, times_list=times_list)
