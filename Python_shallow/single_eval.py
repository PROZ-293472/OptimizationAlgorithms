import TargetFunctions
from Main import optimize
import sys

dim = int(sys.argv[1])
# print(dim)

tf = TargetFunctions.sphere


constr = [(-10, 10) for _ in range(dim)]
max_iter = 200

optimize(objective_function=tf, problem_dimention=dim, plot_data=False,
         algorithm='de', time_eval=False, max_iter=max_iter,
         constraints=constr, constraint_handle='projection')
