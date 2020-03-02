from OptimizationAlgorithms.Python.src.General  import EndConditions as ec
import numpy as np


class DifferentialEvolution:

    DEFAULT_CR = 0.2
    DEFAULT_F = 0.2

    def __init__(self, target_fun, start_pop, f=DEFAULT_F, cr=DEFAULT_CR, maxiter=ec.MAX_ITER):
        self.target_fun = target_fun  # FUNCTOR
        self.population = start_pop  # NUMPY ARRAY OF VECTORS
        self.H = start_pop  # NUMPY ARRAY OF VECTORS
        self.cr = cr  # FLOAT - parameter for crossover
        self.f = f  # FLOAT
        self.eval_time = -1
        self.iterations = 0  # INT
        self.max_iterations = maxiter # INT
        self.end_reason = None  # STRING

    def crossover(self, x, y):
        z = np.empty(1, x.shape[0])
        for i in range(0, x.shape[0]):
            a = np.random.random()
            if a < self.cr:
                z[i] = y[i]
            else:
                z[i] = x[i]
        return z

    def tournament(self, x, y):
        if self.target_fun(x) < self.target_fun(y):
            return x
        else:
            return y

    def run(self):
        t = 0
        while not any([cond for cond in ec.check_end_conditions(i, self.max_iterations, 0, 1).values()]):
            for i in range(0, np.size(self.population, axis=0)):

                # SELECTION - generates a random index from <0,mi> and picks corresponding vector
                r = self.population[np.random.choice(np.size(self.population, axis=0))]
                # SELECTION pt 2 - two random d i s t i n c t points
                d_e = self.population[np.random.choice(np.size(self.population, axis=0), 2, replace=False)]

                M = r + self.f * (d_e[1] - d_e[0])
                O = self.crossover(r, M)

                self.H = np.append(self.H, O)

                self.population[i] = self.tournament(self.population[i], O)
            t += 1






