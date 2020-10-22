from Main import optimize
import TargetFunctions

results = []
for dim in range(5, 50, 5):
    res = optimize(objective_function=TargetFunctions.sphere,
                   problem_dimention=dim, plot_data=False, algorithm='de', time_eval=True)
    results.append({'dim': dim, 'res': res})
print(results)
