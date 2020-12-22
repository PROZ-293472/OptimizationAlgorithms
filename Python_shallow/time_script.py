from Main import optimize
import TargetFunctions
import time
import numpy as np
import matplotlib.pylab as plt

area = (-100, 100)
tf = TargetFunctions.sphere
algorithm = 'cmaes'

results = []
times_netto = {}
rand_points_times = {}
for dim in range(5, 70, 5):
    # calculating fitness of random points
    # max_iter = int(max(1e5, dim*1e4))
    max_iter = 200
    temp_list = []
    for i in range(max_iter):
        point = np.random.uniform(low=area[0], high=area[1], size=(dim,))
        start_time = time.time()
        tf(point)
        temp_list.append(time.time() - start_time)

    mean_rand_point_time = sum(temp_list)/len(temp_list)
    rand_points_times[dim] = mean_rand_point_time
    print(mean_rand_point_time)

    constr = [(-10, 10) for _ in range(dim)]

    res = optimize(objective_function=tf, problem_dimension=dim, plot_data=False,
                   algorithm=algorithm, time_eval=True, max_iter=max_iter,
                   constraints=constr, constraint_handle='projection')

    results.append({'dim': dim, 'res': res})
    times_netto[dim] = res.mean_iteration_time - mean_rand_point_time

# # plotting iteration times by dim
# fig1, ax1 = plt.subplots()
# lists = sorted(times_netto.items())  # sorted by key, return a list of tuples
# x, y = zip(*lists)  # unpack a list of pairs into two tuples
# ax1.set_xlabel('Wymiar')
# ax1.set_ylabel('Czas pojedynczej itareacji [s]')
# ax1.plot(x, y)
# fig1.savefig(f'figs\\time_{algorithm}.png')


# # plotting mean random times by dim
# fig2, ax2 = plt.subplots()
# # sorted by key, return a list of tuples
# lists = sorted(rand_points_times.items())
# x, y = zip(*lists)  # unpack a list of pairs into two tuples
# ax2.set_xlabel('Wymiar')
# ax2.set_ylabel('Czas pojedynczej ewaluacji funkcji celu[s]')
# ax2.plot(x, y)
# fig2.savefig(f'figs\\point_time_{algorithm}.png')

print(results)
