from CMAES import CMAES
from DifferentialEvolution import DifferentialEvolution
from ObjectveFunction import ObjectiveFunction


def optimize(objective_function, problem_dimention, constraints=None, algorithm='cmaes', constraint_handle=None, parameter_dict=None, plot_data=False, time_eval=False, max_iter=None):
    algorithms = {
        'cmaes': CMAES(),
        'de': DifferentialEvolution()
    }

    alg = algorithms[algorithm]
    alg.time_eval = time_eval
    of = ObjectiveFunction(fun=objective_function,
                           bounds=constraints, dim=problem_dimention)
    alg.set_obj_function(of)
    if plot_data:
        assert problem_dimention == 2, 'Plotting works only in 2-dimentional space!'
        alg.enable_plotting()

    if parameter_dict:
        alg.set_parameters(parameter_dict)

    if max_iter:
        alg.max_iter = max_iter
    res = alg.run()
    return res


if __name__ == "__main__":
    import TargetFunctions
    parameters = {'m': (100, 20000)}
    res = optimize(objective_function=TargetFunctions.sphere,
                   problem_dimention=2, plot_data=False, parameter_dict=parameters, algorithm='cmaes', time_eval=True, max_iter=1000)
    print(res)
