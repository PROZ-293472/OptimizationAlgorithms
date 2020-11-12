from Main import optimize
import TargetFunctions
import time
import numpy as np
import matplotlib.pylab as plt

area = (-100, 100)
tf = TargetFunctions.sphere

results = []
times_netto = {}
for dim in range(5, 70, 5):
    # calculating fitness of random points
    rand_points_times = []
    # max_iter = int(max(1e5, dim*1e4))
    max_iter = 200
    for i in range(max_iter):
        point = np.random.uniform(low=area[0], high=area[1], size=(dim,))
        start_time = time.time()
        tf(point)
        rand_points_times.append(time.time() - start_time)

    mean_rand_point_time = sum(rand_points_times)/len(rand_points_times)
    print(mean_rand_point_time)

    res = optimize(objective_function=tf,
                   problem_dimention=dim, plot_data=False, algorithm='cmaes', time_eval=True, max_iter=max_iter)
    results.append({'dim': dim, 'res': res})
    times_netto[dim] = res.mean_iteration_time - mean_rand_point_time

lists = sorted(times_netto.items())  # sorted by key, return a list of tuples
x, y = zip(*lists)  # unpack a list of pairs into two tuples
plt.plot(x, y)
plt.show()
print(results)
