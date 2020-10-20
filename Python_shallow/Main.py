from CMAES import CMAES
from DifferentialEvolution import DifferentialEvolution
from ObjectveFunction import ObjectiveFunction

algorithms = {
    'cmaes': CMAES(),
    'de': DifferentialEvolution()
}


def optimize(objective_function, problem_dimention, constraints=None, algorithm='cmaes', constraint_handle=None, parameter_dict=None, plot_data=False):
    alg = algorithms[algorithm]

    of = ObjectiveFunction(fun=objective_function,
                           bounds=constraints, dim=problem_dimention)
    alg.set_obj_function(of)
    if plot_data:
        assert problem_dimention == 2, 'Plotting works only in 2-dimentional space!'
        alg.enable_plotting()

    if parameter_dict:
        alg.set_parameters(parameter_dict)

    alg.run()
    return alg.sel_best().__dict__, alg.end_reason


if __name__ == "__main__":
    import TargetFunctions
    parameters = {'m': (100, 1000)}
    optimize(objective_function=TargetFunctions.sphere,
             problem_dimention=2, plot_data=False, parameter_dict=parameters, algorithm='cmaes')
