from Main import optimize
import TargetFunctions

switch = 'fixed_iter'

out_dict = {}
c = None
for dim in [3, 5, 10, 20, 50, 70]:
    # for dim in range(1, 50, 5):
    res_dict = {}
    for alg in ['de', 'cmaes', 'des']:
        if switch == 'fixed_iter':
            res = optimize(objective_function=TargetFunctions.rastrigin,
                           problem_dimension=dim, plot_data=False, parameter_dict=None,
                           algorithm=alg, time_eval=False, max_iter=400, constraints=c, constraint_handle='projection')
            res_dict[alg] = "{: 0.3e}".format(res.best_point.value)

        if switch == 'fixed_tol':
            res = optimize(objective_function=TargetFunctions.sphere,
                           problem_dimension=dim, plot_data=False, parameter_dict=None,
                           algorithm=alg, time_eval=False, tolerance=1e-5, max_iter=1e4, constraints=c, constraint_handle='projection')
            res_dict[alg] = res.iteration_num

    out_dict[dim] = res_dict
    str_2_print = f'{dim}'
    for num in res_dict.values():
        str_2_print += f' & $\\num{{{num}}}$'
    str_2_print += ' \\\\'
    print(str_2_print)

print(out_dict)


# print(dim, res.best_point.value)
