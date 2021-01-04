from CMAES import CMAES
from DifferentialEvolution import DifferentialEvolution
from DES import DES
from ObjectveFunction import ObjectiveFunction


def optimize(objective_function, problem_dimension, constraints=None, algorithm='cmaes', constraint_handle=None, parameter_dict=None, plot_data=False, time_eval=False, max_iter=None, tolerance=None):
    algorithms = {
        'cmaes': CMAES(),
        'de': DifferentialEvolution(),
        'des': DES()
    }

    alg = algorithms[algorithm]
    alg.time_eval = time_eval
    of = ObjectiveFunction(fun=objective_function,
                           bounds=constraints, dim=problem_dimension, repair_method=constraint_handle)
    alg.set_obj_function(of)
    if plot_data:
        assert problem_dimension == 2, 'Plotting works only in 2-dimentional space!'
        alg.enable_plotting()

    if parameter_dict:
        alg.set_parameters(parameter_dict)

    if max_iter:
        alg.max_iter = max_iter

    if tolerance:
        alg.tolerance = tolerance
    res = alg.run()
    return res


if __name__ == "__main__":
    import TargetFunctions

    # parameters = {'m': (100, 100)}
    parameters = None
    # c = [(-0.5, 0.5), (-0.5, 0.5)]
    c = None
    # algorithm = 'des'
    for algorithm in ['cmaes']:
        res_list = []
        reps = 30
        for i in range(reps):
            print(i)
            res = optimize(objective_function=TargetFunctions.sphere,
                           problem_dimension=70, plot_data=False, parameter_dict=parameters,
                           algorithm=algorithm, time_eval=True, max_iter=1000, constraints=c, constraint_handle='projection')
            # print(res, res.best_point.value)
            res_list.append(res)

        iter_times = [0 for _ in range(1000)]
        for r in res_list:
            iter_times = [sum(x) for x in zip(iter_times, r.times_list)]
        iter_times = [i/reps for i in iter_times]

        import pickle
        with open(f'Python_shallow\\pickles\\time_list_{algorithm}.pkl', 'wb') as f:
            pickle.dump(iter_times, f)

        import matplotlib.pyplot as plt
        # plotting tim by dim
        plt.xlabel('Iteracja')
        plt.ylabel('średni czas wykonania [s]')
        plt.plot(iter_times)
        plt.grid()
        # plt.savefig(f'Python_shallow\\figs\\iter_time_{algorithm}.png')
