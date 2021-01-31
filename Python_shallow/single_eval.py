import TargetFunctions
from Main import optimize
import sys

alg = str(sys.argv[1])
dim = int(sys.argv[2])

tf = TargetFunctions.sphere


constr = [(-10, 10) for _ in range(dim)]
max_iter = 200


optimize(objective_function=tf, problem_dimension=dim, plot_data=False,
         algorithm=alg, time_eval=False, max_iter=max_iter,
         constraints=constr, constraint_handle='projection')
